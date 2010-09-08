_dodo() {
    local current
    COMPREPLY=()
    current=`_get_cword`

    COMPREPLY=($(compgen -W '$(dodo commands)' -- "$current"))

    return 0
}

complete -F _dodo dodo
