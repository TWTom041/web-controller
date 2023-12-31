import platform
import qrcode
import qrcode.image.svg
import os
import webbrowser

try:
    from pyngrok import conf, ngrok
except ModuleNotFoundError:
    from io import BytesIO
    from zipfile import ZipFile
    from urllib.request import urlopen
    import contextlib
    import os
    import importlib
    import shutil

    @contextlib.contextmanager
    def pushd(new_dir):
        previous_dir = os.getcwd()
        os.chdir(new_dir)
        try:
            yield
        finally:
            os.chdir(previous_dir)

    resp = urlopen("https://github.com/alexdlaird/pyngrok/archive/refs/heads/main.zip")
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.extractall()
    zipfile.close()
    os.rename("pyngrok-main/pyngrok", "pyngrok")
    shutil.rmtree("pyngrok-main")

    print('installed pyngrok')
    ngrok = importlib.import_module("pyngrok.ngrok")
    conf = importlib.import_module("pyngrok.conf")

# dirname = os.path.dirname(__file__)
qr_svg_path = "qr_img.svg"


def qr_terminal_str(str, version=2):
    if platform.system() == "Windows":
        white_block = '██'
        black_block = '  '
        new_line = '\n'
    else:
        white_block = '\033[0;37;47m  '
        black_block = '\033[0;37;40m  '
        new_line = '\033[0m\n'

    qr = qrcode.QRCode(version, image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(str)
    qr.make()
    img = qr.make_image(attrib={'class': ''})
    with open(qr_svg_path, "w") as f:
        f.write(img.to_string(encoding='unicode'))
    # qr.make_image(attrib={'class': ''})
    webbrowser.open(f"file://{os.path.abspath(qr_svg_path)}")

    output = white_block*(qr.modules_count+2) + new_line
    for mn in qr.modules:
        output += white_block
        for m in mn:
            if m:
                output += black_block
            else:
                output += white_block
        output += white_block + new_line
    output += white_block*(qr.modules_count+2) + new_line
    return output

# Setting an auth token allows us to open multiple
# tunnels at the same time
auth = input("Auth token:")
if auth:
    ngrok.set_auth_token(auth)

port = input("Port:")
port = port if port else 5002
http_https = "https"
print("Using {}".format(http_https))
region = input("Region:")
conf.get_default().region = region if region else "jp"

ngrok_tunnel = ngrok.connect(f"https://127.0.0.1:{port}")
print(ngrok_tunnel.public_url)
print(qr_terminal_str(ngrok_tunnel.public_url))
print(f"svg saved at {os.path.abspath(qr_svg_path)}")
print("Press enter to exit")
input()
ngrok.kill()
