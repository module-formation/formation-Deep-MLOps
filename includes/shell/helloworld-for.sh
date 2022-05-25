read -p "What's your name ? " user

if [ $user = mathieu ]
  then
  echo "Hello World shell, it's $user"
  for item in $(cat list.txt)
    do
    echo $item
    done
else
  echo "Hello stranger !"
fi