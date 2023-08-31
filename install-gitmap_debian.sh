echo "       ____________________________"
echo "       ||          _____         ||"
echo "       ||         < $ $ >        ||"
echo "       ||     ___  \ . /         ||"
echo "       ||        \ |   |         ||"
echo "       ||         / \  /\        ||"
echo "       ||        _\-----/_       ||"
echo "       ||________________________||"
echo "    =================================="
echo ""
echo "[+] Starting the installation of GitMap..."

sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip
pip3 install click colorama requests
chmod +x ./gitmap.py
sudo cp ./gitmap.py /usr/bin/gitmap

echo "[+] Setup finished"
echo "[*] run 'gitmap --help' to see what you can do with it."