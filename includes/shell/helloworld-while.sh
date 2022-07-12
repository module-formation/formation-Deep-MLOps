read -p "What's your name ? " user

while [ $user = mathieu ]
do
  echo "Hello World shell, it's $user"
  for item in $(cat list.txt)
    do
    echo $item
    done
  read -p "What's your name ? " user
done
exit
