#!/bin/bash

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            before) BEFORE=${VALUE} ;;
            after)  AFTER=${VALUE} ;;     
            *)   
    esac    
done

echo "attempting to compare '$BEFORE' with '$AFTER'"

# ensure earlier revision supports comparison
git merge-base --is-ancestor ffece23fabe9d7698519dea4d62be959bc73d8cf $BEFORE
SUPPORTS_COMPARISON=$?

# ensure later revision is derived from earlier revision
git merge-base --is-ancestor $BEFORE $AFTER
CORRECT_ORDER=$?

if [ $SUPPORTS_COMPARISON -ne 0 ] ; then
    echo "$BEFORE is too old to support comparison"
    exit 1
fi

if [ $CORRECT_ORDER -ne 0 ]; then
    echo "$BEFORE is not an ancestor of $AFTER, comparison not possible"
    exit 1
fi
