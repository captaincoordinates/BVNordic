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

git merge-base --is-ancestor 6d83605ae2c2dbf1610441b5c816f942198ae747 $BEFORE
SUPPORTS_COMPARISON=$?

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
