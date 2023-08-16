<script>

    import {onMount} from "svelte";


    import npyjs from "npyjs";
    import {strFromU8, unzipSync} from "fflate";
    import {cosineSimilarity} from "vector-cosine-similarity";
    import Loading from "$lib/Loading.svelte";
    import Tokenizer from "clip-bpe-js";
    import RangeSlider from "$lib/RangeSlider.svelte";


    // let n = new npyjs();
    // const query = url.searchParams.get('query')


    export let data;
    let loading = false;
    let results = [];
    $: displayResults = results.filter(r => {
        return ((r.score >= (scoreRangeValues[0] + scoreRangeDisplay[0] * (scoreRangeValues[1] - scoreRangeValues[0]))) &&
            (r.score <= (scoreRangeValues[0] + scoreRangeDisplay[1] * (scoreRangeValues[1] - scoreRangeValues[0]))) &&
            (r.created_utc >= (dateRangeValues[0] + dateRangeDisplay[0] * (dateRangeValues[1] - dateRangeValues[0]))) &&
            (r.created_utc <= (dateRangeValues[0] + dateRangeDisplay[1] * (dateRangeValues[1] - dateRangeValues[0]))));
    }).slice(0, 100);

    let dateRangeDisplay = [0, 1]
    let scoreRangeDisplay = [0, 1]

    let dateRangeValues = []
    let scoreRangeValues = [];


    const displayDate = d => {
        if ((!d && d !== 0) || (dateRangeValues.length !== 2)) return '';
        const utcDate = d * (dateRangeValues[1] - dateRangeValues[0]) + dateRangeValues[0];
        return new Date(utcDate * 1000).toLocaleDateString();
    }

    const displayScore = d => {
        if ((!d && d !== 0) || (scoreRangeValues.length !== 2)) return '';
        return Math.round(d * (scoreRangeValues[1] - scoreRangeValues[0]) + scoreRangeValues[0]);
    }
    onMount(async () => {
        await getResults();
    })


    async function getResults() {
        loading = true;


        // Begin Comment Zone

        console.log('Model Loading')
        if (self.crossOriginIsolated) { // needs to be cross-origin-isolated to use wasm threads. you need to add these two headers: https://web.dev/coop-coep/
            ort.env.wasm.numThreads = navigator.hardwareConcurrency
        }
        const modelPath = 'https://huggingface.co/rocca/openai-clip-js/resolve/main/clip-text-vit-32-float32-int32.onnx';
        let session = await ort.InferenceSession.create(modelPath, {
            executionProviders: ["wasm"]
        });
        console.log("Model loaded.");
        let tokenizer = new Tokenizer();
        let queryToken = tokenizer.encodeForCLIP(data.query);
        console.log('Returning', queryToken)
        let encodedQueryToken = Int32Array.from(queryToken);
        const feeds = {'input': new ort.Tensor('int32', encodedQueryToken, [1, encodedQueryToken.length])};
        console.log('Running Infer')
        const modelResults = await session.run(feeds);
        const output = modelResults.output.data;
        console.log('Infer Complete', output);

        // Done Comment Zone

        // let output = new Float32Array(512).fill(0.5);

        let n = new npyjs();

        const compressedVectors = await fetch('/vector_matrix.npy.zip');
        const compressedVectorsBuffer = await compressedVectors.arrayBuffer();
        const unzipped = unzipSync(new Uint8Array(compressedVectorsBuffer));
        const vectors = n.parse(unzipped['vector_matrix.npy'].buffer);
        const mappingReq = await fetch('/indexed_vectors.json');
        const indexMapping = await mappingReq.json();

        const compressedCommentsReq = await fetch('/comments.json.zip');
        const compressedCommentsArrayBuffer = await compressedCommentsReq.arrayBuffer();
        const unzippedComments = unzipSync(new Uint8Array(compressedCommentsArrayBuffer));
        const comments = JSON.parse(strFromU8(unzippedComments['comments.json'].buffer));

        console.log(comments['134qgb0_jigatxs'])


        let minScore = Infinity;
        let maxScore = -Infinity;
        let minCreatedUtc = Infinity;
        let maxCreatedUtc = -Infinity;
        // Get Index of Closest Matches
        // Read JSON from file
        const size = 512;
        let distances = Object.entries(indexMapping).map(e => {
            let [key, value] = e;
            let vectorIndex = value.vector;
            let vector = vectors.data.slice(vectorIndex * size, (vectorIndex + 1) * size);

            const similarity = cosineSimilarity(vector, output);
            const commentId = `${value.post_id}_${value.comment_id}`
            const commentData = comments[commentId]
            minScore = Math.min(minScore, commentData['score']);
            maxScore = Math.max(maxScore, commentData['score']);
            minCreatedUtc = Math.min(minCreatedUtc, commentData['created_utc']);
            maxCreatedUtc = Math.max(maxCreatedUtc, commentData['created_utc']);
            return {
                'id': key,
                similarity,
                post_id: value.post_id,
                comment_id: value.comment_id,
                url: value.url, ...commentData
            }
        })
        scoreRangeValues = [minScore, maxScore];
        dateRangeValues = [minCreatedUtc, maxCreatedUtc];
        distances.sort((a, b) => b.similarity - a.similarity);
        results = distances;
        loading = false;
    }


    function markdownToHTML(markdown) {
        // Replace newlines with line breaks
        let html = markdown.replace(/\n/g, '<br/>');

        // Replace Markdown-style links with HTML links
        html = html.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2">$1</a>');

        return html;
    }

</script>
<style>


    #back-button-text {
        font-family: 'Knewave', cursive;
        color: white;
        padding: 0 15px;
        border-radius: 4px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.2s ease-out;
    }

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
        width: 70vw;
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
        font-size: 5em;
        padding: 0;
        margin: 0;
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
        justify-content: space-between;
        width: 70vw;
        flex-direction: row;
    }

    .slider-label {
        display: flex;
        justify-content: center;
        /*   bold */

    }

    .sliders-container * {
        font-family: 'Instrument Sans', sans-serif;
    }

    .slider-label-text {
        font-weight: bold;
    }
</style>

<!--<div id="back-button">-->
<!--    <a on:click={back} style="text-decoration:none"><h1 id="back-button-text">Back</h1></a>-->
<!--</div>-->

{#if loading}
    <Loading/>
{:else}
    <!--Iterate over data.matches-->
    <div class="container">
        <h1>Results</h1>
        <div class="sliders-container">
            <div class="slider-container">
                <div class="slider-label">
                    <span class="slider-label-text">Date</span>
                </div>
                <RangeSlider bind:start={dateRangeDisplay[0]} bind:end={dateRangeDisplay[1]}/>
                <div class="labels">
                    <div class="label">{displayDate(dateRangeDisplay[0])}</div>
                    <div class="label">{displayDate(dateRangeDisplay[1])}</div>
                </div>
            </div>
            <div class="slider-container">
                <div class="slider-label">
                    <span class="slider-label-text">Score</span>
                </div>
                <RangeSlider bind:start={scoreRangeDisplay[0]} bind:end={scoreRangeDisplay[1]}/>
                <div class="labels">
                    <div class="label">{displayScore(scoreRangeDisplay[0])}</div>
                    <div class="label">{displayScore(scoreRangeDisplay[1])}</div>
                </div>
            </div>
        </div>
        <table>
            <tr>
                <th></th>
                <th>Score</th>
                <th>Thread</th>
                <th>Comment</th>
                <th>Image</th>
            </tr>
            {#if !results || results?.length === 0}
                <tr>
                    <td colspan="4">
                        <div class="table-content">
                            No results found
                        </div>
                    </td>
                </tr>
            {/if}
            {#each displayResults || [] as match}
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
                            <a href={`https://reddit.com${match.link}`}>Thread</a>
                        </div>
                    </td>
                    <td>
                        <div class="table-content">
                            {@html markdownToHTML(match.body)}
                        </div>
                    </td>
                    <td>
                        <div class="table-content">
                            <a href="{match.url}" target="_blank"> <img class="resize" src="{match.url}" alt="Outfit"/></a>
                        </div>
                    </td>
                </tr>
            {/each}
        </table>
    </div>

{/if}