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

pkg update && pkg upgrade -y
pkg install python3 -y
pip install click colorama requests
chmod +x ./gitmap.py
cp ./gitmap.py $PREFIX/bin/gitmap

echo "[+] Setup finished"
echo "[*] run 'gitmap --help' to see what you can do with it."