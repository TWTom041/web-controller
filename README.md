# web-controller
This repo is for controlling mouse and keyboard for windows, macos, and linux (based on what PyAutoGUI supports)

### Use Cases
Have you ever wanted to control your computer remotely but without a keyboard or mouse near you? This project can just do just that. What's even better? Thanks to the web based interface, you can just install just one program on the device you want to control, no more executables needed on the controller client. 

### How to use
1. Clone this repo
```bash
git clone https://github.com/TWTom041/web-controller.git
```
2. Install Python
3. Change the password in main.py to what you want \
![image](https://github.com/TWTom041/web-controller/assets/57289975/2076706c-acf2-4914-8255-237e3eda6c55)
4. (Optional) Change the host to 0.0.0.0 to listen on all addresses \
![image](https://github.com/TWTom041/web-controller/assets/57289975/b099c76c-a879-4682-bdda-3fdb90336a60)
5. (Optional) Add SSL key yourself to enable HTTPS, or adhoc if you want
6. Install requirements.txt
```bash
pip install -r requirements.txt
```
8. Run main.py
```bash
python main.py
```
9. (Optional) Use Ngrok or other tunnelling service if you want to publicly access the server inside NAT
10. Go to the server IP and login \
![image](https://github.com/TWTom041/web-controller/assets/57289975/602f7c4c-2fa4-4e9b-be02-359271a9376e) \
![image](https://github.com/TWTom041/web-controller/assets/57289975/d942aa3c-97ff-4bd6-b87e-5b68ea7e624c)

### TODO
1. Multi-Users support
2. Add mouse click support
3. Add keyboard input support
4. Solve interaction latency problem
