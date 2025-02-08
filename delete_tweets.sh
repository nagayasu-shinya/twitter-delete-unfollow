#!/bin/bash -eu
#
# Delete tweets.
#
# shellcheck disable=SC2312

set -o pipefail
shopt -s inherit_errexit

readonly DO_NOT_DELETE_TWEETS_TXT='do_not_delete_tweets.txt'

function usage() {
    echo ""
    echo "Usage: bash $0 [--dry-run] [--retweets]"
    echo "   Delete tweets."
    echo ""
    echo "  Options:"
    echo "    --retweets maximum retweet count, defalut 100"
    echo "    --favs     maximum favarites count, defalut 100"
    echo "    --dry-run  enable dry-run"
}

function main() {
    if [[ ! -f "${DO_NOT_DELETE_TWEETS_TXT}" ]]; then
        echo "${DO_NOT_DELETE_TWEETS_TXT} is not found."
        exit 1
    fi

    local max_retweets=''
    local max_favs=''
    local dry_run=''
    TEMP=$(getopt --options 'h' --longoptions help,dry-run,retweets:,favs: -- "$@")
    # shellcheck disable=SC2181
    if [[ $? != 0 ]]; then
        echo "Invalid argments $*" >&2
        usage >&2
        exit 1
    fi

    eval set -- "$TEMP"
    while true ; do
        case "$1" in
        -h | --help) usage; exit 0 ;;
        --dry-run) dry_run="$1" ; shift 1 ;;
        --retweets) max_retweets="$2" ; shift 2 ;;
        --favs) max_favs="$2" ; shift 2 ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
        esac
    done

    # shellcheck disable=SC2086
    python delete_tweets.py --retweets="${max_retweets:-100}" --favs="${max_favs:-100}" --do-not-delete="${DO_NOT_DELETE_TWEETS_TXT}" ${dry_run:-}
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
