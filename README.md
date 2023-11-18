# web-controller
This repo is for controlling mouse and keyboard for Windows, MacOS, and Linux (based on what PyAutoGUI supports)

### Use Cases
Have you ever wanted to control your computer remotely without a keyboard or mouse near you? This project can do just that. What's even better? Thanks to the web-based interface, you can install just one program on the device you want to control, no more executables are needed on the controller client. 

### How to use
1. Clone this repo
```bash
git clone https://github.com/TWTom041/web-controller.git
```
2. Install Python
3. Change the password in main.py to what you want
```bash
python set_password.py
```
> [!NOTE] 
> The initial password is "randompassword"
4. (Optional) Add SSL key yourself to enable HTTPS, or adhoc if you want. 
> [!WARNING] 
> Don't set it to None to prevent sending plain-text password
5. Install requirements.txt
```bash
pip install -r requirements.txt
```
6. Run main.py
```bash
python main.py
```
7. (Optional) Use Ngrok or other tunnelling service if you want to publicly access the server inside NAT
8. Navigate to the server IP and login \
![image](https://github.com/TWTom041/web-controller/assets/57289975/602f7c4c-2fa4-4e9b-be02-359271a9376e) \
![image](https://github.com/TWTom041/web-controller/assets/57289975/d942aa3c-97ff-4bd6-b87e-5b68ea7e624c)

### TODO
1. Multi-Users support
2. Add keyboard input support
