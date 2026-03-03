from flask import Flask, request, redirect, url_for, send_from_directory
import pandas as pd
import os
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# ---------------- 首页：上传 + 文件列表 ----------------
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return f'''
    <h1>迷你网盘 + 在线运算</h1>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file">
      <button>上传</button>
    </form>
    <ul>
    {''.join(
        f'<li>{f} '
        f'<a href="/download/{f}">下载</a> | '
        f'<a href="/analyze/{f}">分析</a> | '
        f'<a href="/delete/{f}">删除</a></li>'
        for f in files
    )}
    </ul>
    '''

# ---------------- 上传 ----------------
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename == '':
        return '没选文件'
    # 只让 csv/xlsx 通过（简单校验）
    if not file.filename.lower().endswith(('.csv', '.xlsx')):
        return '请上传 .csv 或 .xlsx'
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    return redirect('/')

# ---------------- 下载 ----------------
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ---------------- 删除 ----------------
@app.route('/delete/<filename>')
def delete(filename):
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return redirect('/')

# ---------------- 分析 ----------------
@app.route('/analyze/<filename>')
def analyze(filename):
    in_path = os.path.join(UPLOAD_FOLDER, filename)
    out_name = f"report_{int(time.time())}.csv"
    out_path = os.path.join(RESULT_FOLDER, out_name)

    # 读数据
    if filename.lower().endswith('.csv'):
        df = pd.read_csv(in_path)
    else:
        df = pd.read_excel(in_path)

    # 算统计
    report = {
        '行数': [len(df)],
        '列数': [len(df.columns)],
        '数值列平均': [df.select_dtypes(include='number').mean().mean()],
        '数值列最大': [df.select_dtypes(include='number').max().max()],
        '数值列最小': [df.select_dtypes(include='number').min().min()],
    }

    # 写结果
    pd.DataFrame(report).to_csv(out_path, index=False)
    return f'''
    <h2>分析完成</h2>
    <p>原始文件：{filename}</p>
    <p>行数：{len(df)}，列数：{len(df.columns)}</p>
    <a href="/result/{out_name}">下载统计报告</a>
    <br><br>
    <a href="/">返回网盘</a>
    '''

# ---------------- 结果下载 ----------------
@app.route('/result/<filename>')
def result_download(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)