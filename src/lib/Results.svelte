<!--<script>-->
<!--    import {onMount} from 'svelte';-->
<!--    import {browser} from '$app/environment';-->
<!--    import npyjs from "npyjs";-->

<!--    export let comments;-->
<!--    export let indexMapping;-->
<!--    export let vectors;-->

<!--    let matches = [];-->


<!--    onMount(async ({ fetch}) => {-->
<!--        if (browser) {-->

<!--            // let n = new npyjs();-->
<!--            // const query = url.searchParams.get('query')-->
<!--            // // Load index mapping from JSON-->
<!--            const indexMapping = JSON.parse(fetch('static/index_mapping.json'));-->
<!--            console.log( indexMapping);-->

<!--            // const compressedVectors = fs.readFileSync('static/vector_matrix.npy.gz');-->
<!--            // const decompressedVectors = await gunzip(compressedVectors);-->
<!--            // const vectors = n.parse(decompressedVectors.buffer);-->
<!--            //-->
<!--            // const compressedData = fs.readFileSync('static/comments.json.gz');-->
<!--            // const decompressedData = await gunzip(compressedData);-->
<!--            // const comments = JSON.parse(decompressedData.toString());-->
<!--            //-->
<!--            // return {-->
<!--            //     comments, 'vectors': Array.from(vectors.data), indexMapping, query-->
<!--            // }-->
<!--            // console.log('Browsing,');-->

<!--            // if (self.crossOriginIsolated) { // needs to be cross-origin-isolated to use wasm threads. you need to add these two headers: https://web.dev/coop-coep/-->
<!--            //     ort.env.wasm.numThreads = navigator.hardwareConcurrency-->
<!--            // }-->
<!--            // const modelPath = 'https://huggingface.co/rocca/openai-clip-js/resolve/main/clip-text-vit-32-float32-int32.onnx';-->
<!--            // let session = await ort.InferenceSession.create(modelPath, {-->
<!--            //     executionProviders: ["wasm"]-->
<!--            // });-->
<!--            // console.log("Model loaded.");-->
<!--            // console.log('Returning')-->
<!--            // let tokenizer = new Tokenizer();-->
<!--            // // let queryToken = tokenizer.encodeForCLIP(url.searchParams.get('query'));-->
<!--&lt;!&ndash;            // let queryToken = tokenizer.encodeForCLIP("Simon");&ndash;&gt;-->
<!--            // let encodedQueryToken = Int32Array.from(queryToken);-->
<!--            // const feeds = {'input': new ort.Tensor('int32', encodedQueryToken, [1, encodedQueryToken.length])};-->
<!--            // console.log('Running Infer')-->
<!--            // const results = await session.run(feeds);-->
<!--            // const output = results.output.data;-->
<!--            // console.log(output);-->


<!--            // let minScore = Infinity;-->
<!--            // let maxScore = -Infinity;-->
<!--            // let minCreatedUtc = Infinity;-->
<!--            // let maxCreatedUtc = -Infinity;-->
<!--            // const start = Date.now();-->
<!--            // // Get Index of Closest Matches-->
<!--            // // Read JSON from file-->
<!--            // const size = 512;-->
<!--            // let distances = Object.entries(indexMapping).map(e => {-->
<!--            //     let [key, value] = e;-->
<!--            //     let vectorIndex = value.vector;-->
<!--            //     let vector = vectors.slice(vectorIndex * size, (vectorIndex + 1) * size);-->
<!--            //-->
<!--            //     const similarity = cosineSimilarity(vector, output);-->
<!--            //     const commentId = `${value.post_id}_${value.comment_id}`-->
<!--            //     const commentData = comments[commentId]-->
<!--            //     minScore = Math.min(minScore, commentData['score']);-->
<!--            //     maxScore = Math.max(maxScore, commentData['score']);-->
<!--            //     minCreatedUtc = Math.min(minCreatedUtc, commentData['created_utc']);-->
<!--            //     maxCreatedUtc = Math.max(maxCreatedUtc, commentData['created_utc']);-->
<!--            //     return {-->
<!--            //         'id': key,-->
<!--            //         similarity,-->
<!--            //         post_id: value.post_id,-->
<!--            //         comment_id: value.comment_id,-->
<!--            //         url: value.url, ...commentData-->
<!--            //     }-->
<!--            // })-->
<!--            // distances.sort((a, b) => b.similarity - a.similarity);-->
<!--            // console.log()-->
<!--            // matches = distances;-->


<!--        } else {-->
<!--            console.log('Not browsing')-->
<!--        }-->
<!--    });-->

<!--</script>-->

<!--<style>-->
    .container {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: start;
        align-items: center;
        flex-direction: column;
    }

    table {
        border-collapse: separate;
        border-spacing: 0;
        background-color: white;
        width: 50vw;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #dddddd;
    }

    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }

    .table-content {
        max-height: 220px;
        width: 100%;
        overflow-y: auto;
    }

    h1 {
        text-align: center;
        font-family: 'Knewave', cursive;
        color: #FF5A5F;
    }

    table * {
        font-family: 'Instrument Sans', sans-serif;
    }

    .resize {
        height: 200px;
        width: auto;
    }

    .label:first-child {
        float: left;
    }

    .label:last-child {
        float: right;
    }

    .slider-container {
        width: 200px;
        margin: 0 20px;
    }

    .sliders-container {
        display: flex;
        justify-content: center;
    }

    #back-button {
        position: absolute;
        top: 0;
        left: 0;
        margin: 0 25px;
        color: white;
        text-decoration: none;

    }

    #back-button-text:hover {
        background-color: #7a7a7a;
    }

    #back-button-text {
        font-family: 'Knewave', cursive;
        color: white;
        padding: 0 15px;
        border-radius: 4px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.2s ease-out;
    }
<!--</style>-->

<div id="back-button">
    <a href="/" style="text-decoration:none"><h1 id="back-button-text">Back</h1></a>
</div>

<!--Iterate over data.matches-->
<div class="container">
    <h1>Results</h1>
    <!--    <div class="sliders-container">-->
    <!--        <div class="slider-container">-->
    <!--            <RangeSlider bind:start bind:end/>-->
    <!--            <div class="labels">-->
    <!--                <div class="label">{nice(start)}</div>-->
    <!--                <div class="label">{nice(end)}</div>-->
    <!--            </div>-->
    <!--        </div>-->
    <!--        <div class="slider-container">-->
    <!--            <RangeSlider bind:start bind:end/>-->
    <!--            <div class="labels">-->
    <!--                <div class="label">{nice(start)}</div>-->
    <!--                <div class="label">{nice(end)}</div>-->
    <!--            </div>-->
    <!--        </div>-->
    <!--    </div>-->
    <table>
        <tr>
            <th></th>
            <th>Upvotes</th>
            <th>Comment</th>
            <th>Image</th>
        </tr>
        {#each matches.slice(0, 20) as match}
            <tr>
                <td>
                    <div class="table-content">
                        {match.similarity.toFixed(2)}
                    </div>
                </td>
                <td>
                    <div class="table-content">
                        {match.score}
                    </div>
                </td>
                <td>
                    <div class="table-content">
                        {@html markdownToHTML(match.body)}
                    </div>
                </td>
                <td>
                    <div class="table-content">
                        <a href="{match.url}" target="_blank"> <img class="resize" src="{match.url}"
                                                                    alt="Outfit"/></a>
                    </div>
                </td>
            </tr>
        {/each}
    </table>
</div>
