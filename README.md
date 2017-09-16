# rad-control

# Arduino
mkdir -p arduino/ext
cd arduino/ext
git clone https://github.com/PaulStoffregen/OneWire.git
git clone https://github.com/milesburton/Arduino-Temperature-Control-Library.git
cd ../
make
make upload