#!/bin/bash -eu
#
# Delete favorites.
#
# Delete favorites.
# This script requires like.js
# included in the Twitter archive file.
#
# shellcheck disable=SC2312

set -o pipefail
shopt -s inherit_errexit

readonly LIKE_JS='like.js'

function usage() {
    echo ""
    echo "Usage: bash $0 [--dry-run]"
    echo "   Delete all favarites."
    echo ""
    echo "  Options:"
    echo "    --dry-run  enable dry-run"
}

function get_favorite_id() {
    grep tweetId "$1" | cut -d':' -f2 | tr -d ' ,"'
}

function main() {
    if [[ ! -f "${LIKE_JS}" ]]; then
        echo "${LIKE_JS} is not found."
        exit 1
    fi

    local dry_run=''
    TEMP=$(getopt --options 'h' --longoptions help,dry-run -- "$@")
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
        --) shift ; break ;;
        *) echo "Internal error!" ; exit 1 ;;
        esac
    done

    local favorite_id
    favorite_id=$(get_favorite_id "${LIKE_JS}")

    # shellcheck disable=SC2086
    python delete_favorites.py <(cat <<< "${favorite_id}") ${dry_run:-}
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
