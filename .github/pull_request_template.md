# Testing Pull Request Template Scripting

<script type="text/javascript">

    const rootFolderId = "12KXNQnznMe9dkuqOJwXF8N0Ka1IartxL";
    const folderMimeType = "application/vnd.google-apps.folder";
    const compareDirName = "compare-89ea744afcdf9154be689184c6cf579b76ac7b94-d6d331ba2b3fbd304c08ce47c83dd50e52f4d6e3";
    const apiKey = "AIzaSyBQyI3kAjHgLVM4ZQFjJK_BsBKkFTul6mQ";
    const apiUrlRoot = "https://www.googleapis.com/drive/v3";
    const existCheckTimer = 5000;
    let exists = false;
    let files = null;

    function onLoad() {
        const existsCheck = () => {
            getDir(compareDirName, rootFolderId, true)
                .then(dir => {
                    if (dir === null) {
                        window.setTimeout(existsCheck, existCheckTimer);
                    } else {
                        exists = true;
                        getFilesInfo(dir);
                    }
                })
        };
        existsCheck();
    }

    function getDir(dirName, parentId, allowMultiple = false) {
        return fetch([
            apiUrlRoot,
            "/files?",
            [
                `q='${parentId}' in parents and mimeType='${folderMimeType}' and name = '${dirName}'`,
                `key=${apiKey}`
            ].join("&")
        ].join(""))
            .then(response => response.json())
            .then(data => {
                switch (data.files.length) {
                    case 0:
                        return null;
                    case 1:
                        return data.files[0];
                    default:
                        if (allowMultiple) {
                            return data.files[0];
                        }
                        else {
                            throw Error(`Unexpected # dir results (${data.files.length})`);
                        }
                }
            })
        ;
    }

    // function getDirs(parentId) {
    //     return fetch([
    //         apiUrlRoot,
    //         "files?",
    //         [
    //             `q=${parentId} in parents and mimeType='${folderMimeType}'`
    //             `key=${apiKey}`
    //         ].join("&")
    //     ])
    //         .then(response => response.json())
    //         .then(data => data.files)
    //     ;
    // }

    function getFile(parentId, fileName) {

    }

    function getFilesInfo(compareDir) {
        getDir("result", compareDir.id)
            .then(resultDir => {
                if (resultDir === null) {
                    return;   
                }
                else {
                    console.log(resultDir);
                }
            })
        ;
    }

    onLoad();
    
</script>
