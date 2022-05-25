while true
do
    echo "1"
    echo "2"
    echo "3"
    read -p "Enter your choice : " choice

    case $choice in

        1) echo 1
        ;;
        2) echo 2
        ;;
        3) break
        ;;
        *) continue
        ;;
    esac
done

