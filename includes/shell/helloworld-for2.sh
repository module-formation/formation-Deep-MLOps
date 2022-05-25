
read -p "What's your name ? " user

if [ $user = mathieu ]
  then
  echo "Hello World shell, it's $user"
  for item in {1..5}
    do
    echo $item
    done
else
  echo "Hello stranger !"
fi