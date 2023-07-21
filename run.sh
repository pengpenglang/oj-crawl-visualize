#/bin/bash
ecal "cd scripts/"
eval "python3 ./hdu.py"
echo "hdu.py executed at $(date)"
eval "python3 ./nowcoder.py"
echo "nowcoder.py executed at $(date)"
#等待退出
read -p "Press any key to continue..."
