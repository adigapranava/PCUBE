echo "Build Start"
python3.9 -m pip install -r requirements.txt
echo "install End"
python3.9 manage.py collectstatic
echo "Build End"