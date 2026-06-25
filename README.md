A POSIX ACL to NFSv4 ACL migration utility.

Features

✓ POSIX ACL parser
✓ NFSv4 ACL translator
✓ Recursive migration
✓ Dry-run mode
✓ Rollback support
✓ Logging
✓ Validation
✓ JSON reports
✓ Unit tests
✓ Packaging

To run this :

python3 aclmigrate.py \
    --source /mnt/nfs3/test.txt \
    --destination /mnt/nfs4/test.txt