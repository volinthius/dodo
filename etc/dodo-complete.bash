_dodo() {
    local current
    local prev

    COMPREPLY=()

    cur=`_get_cword`
    prev=${COMP_WORDS[COMP_CWORD - 1]}

    if [ $COMP_CWORD -gt 2 ]; then
	return 0
    fi

    case "$prev" in
	ls|add)
	    COMPREPLY=($(compgen -W '$(dodo --no-colors projects)' -- "$cur"))
	    ;;

	archive|help|commands|do|dl|pri|projects|rm|version)
	    ;;

	*)
	    COMPREPLY=($(compgen -W '$(dodo commands)' -- "$cur"))
	    ;;
    esac


    return 0
}

complete -F _dodo dodo
