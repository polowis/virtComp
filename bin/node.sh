isNodeInstalled(){
    if which node > /dev/null
    then
        echo "node is installed, skipping... Make sure you have the latest version of node"
        return 0
    else
        echo "node is not installed. Make sure you have the latest version of node"
        return 1
    fi
}