for i in {1..100}; do curl 127.0.0.1:8000/display?gender=0; curl 127.0.0.1:8000/display?gender=1; done