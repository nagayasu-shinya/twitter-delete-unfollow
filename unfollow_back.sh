#!/bin/bash -eu
#
# Unfollow back.
#
# Unfollow accounts that are not followers.
# This script requires following.js and follower.js
# included in the Twitter archive file.
# Accounts you do not want to unfollow
# should be listed in a do_not_unfollow.txt.
#
# shellcheck disable=SC2312

set -o pipefail
shopt -s inherit_errexit

readonly DO_NOT_UNFOLLOW_TXT='do_not_unfollow.txt'
readonly FOLLOWING_JS='following.js'
readonly FOLLOWER_JS='follower.js'

function usage() {
    echo ""
    echo "Usage: bash $0 [--dry-run]"
    echo "   Unfollow accounts that are not followers."
    echo ""
    echo "  Options:"
    echo "    --dry-run  enable dry-run"
}

function get_unfollowed (){
    diff -u <(grep accountId "$1" | cut -d':' -f2 | tr -d '",' | sort -n) \
            <(grep accountId "$2" | cut -d':' -f2 | tr -d '",' | sort -n) \
            | grep "^+ " | tr -d '+ '
}

function get_unfollow_user() {
    diff -u <(sort -n "${DO_NOT_UNFOLLOW_TXT}") <(cat <<< "${unfollowers}" | sort -n) | tail -n +4 | grep "^+" | tr -d '+'
}

function main() {
    if [[ ! -f "${FOLLOWING_JS}" || ! -f "${FOLLOWER_JS}" ]]; then
        echo "${FOLLOWING_JS} or ${FOLLOWER_JS} is not found."
        exit 1
    fi
    if [[ ! -f "${DO_NOT_UNFOLLOW_TXT}"  ]]; then
        echo "${DO_NOT_UNFOLLOW_TXT} is not found."
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

    local unfollowers
    unfollowers=$(get_unfollowed "${FOLLOWER_JS}" "${FOLLOWING_JS}")

    local unfollow_user
    unfollow_user=$(get_unfollow_user "${DO_NOT_UNFOLLOW_TXT}" "${unfollowers}")

    # shellcheck disable=SC2086
    python unfollow.py <(cat <<< "${unfollow_user}") ${dry_run:-}
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
