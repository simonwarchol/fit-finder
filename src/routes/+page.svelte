<script>
    import Loading from "$lib/Loading.svelte";
    import { navigating } from '$app/stores'
    console.log('Here')

</script>
<style>


    input {
        display: flex;
        padding: 15px;
        margin-bottom: 17vh;
        background-color: white;
        border: 2px solid black;
        color: #111;
        font-size: 15px;
        width: 600px;
        box-shadow: 3px 1px 0px 2px, 0px -1px 0px 2px rgba(0, 0, 0, 0.62);
        height: 30px;
        transform: skew(-3deg, 1deg);
        font-family: 'Knewave', cursive;
        letter-spacing: 2px;
        text-transform: uppercase;
    }


</style>
{#if $navigating}
    <Loading/>
{:else}
    <form method="GET" action="/search">
        <input type="text" name="query" required>
    </form>
{/if}




