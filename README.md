# web-controller
This repo is for controlling mouse and keyboard for windows, macos, and linux (based on what PyAutoGUI supports)

### Use Cases
Have you ever wanted to control your computer remotely but without a keyboard or mouse near you? This project can just do just that. What's even better? Thanks to the web based interface, you can just install just one program on the device you want to control, no more executables needed on the controller client. 

### How to use
1. Clone this repo
2. Install Python
3. Change the password in main.py to what you want
4. (Optional) Change the host to 0.0.0.0 to listen on all addresses
5. (Optional) Add SSL key yourself to enable HTTPS, or adhoc if you want
6. Install requirement.txt
7. Run main.py
8. (Optional) Use Ngrok or other tunnelling service if you want to publicly access the server inside NAT
9. Go to the server IP and login

### TODO
1. Multi-Users support
2. Add mouse click support
3. Add keyboard input support
4. Solve interaction latency problem
