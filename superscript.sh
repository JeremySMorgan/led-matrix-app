#/home/pi/Desktop/led_interface/ngrok start --config=/home/pi/.ngrok2/ngrok.yml led_interface & 
#python ~/Desktop/led_interface/app.py 
/home/pi/Desktop/led_interface/ngrok start --config=/home/pi/.ngrok2/ngrok.yml led_interface &
python ~/Desktop/led_interface/app.py 

# sudo /etc/init.d/led_matrix_superscript start
