<script>
    import fit from '$lib/img/fit.svg';
    import {navigating} from '$app/stores'
    import Loading from '$lib/Loading.svelte'
</script>
<style>
    @font-face {
        font-family: 'Knewave';
        font-weight: normal;
        font-style: normal;
        font-display: swap;
        src: url('/fonts/Knewave-Regular.ttf'); /* IE9 Compat Modes */
    }

    @font-face {
        font-family: 'Instrument Sans', sans-serif;
        font-weight: normal;
        font-style: normal;
        font-display: swap;
        src: url('/fonts/InstrumentSans.ttf'); /* IE9 Compat Modes */
    }


    .fit-container {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: auto;
    }

    .center-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh; /* Set the container height to 100% of the viewport height */
    }

    img#fit {
        height: 100vh;
    }

    #background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #ACC3A6;
        opacity: 1; /* Opacity of the div */
        z-index: -1; /* Place the div behind other elements */
        pointer-events: none; /* Disable pointer events for the div */
    }


</style>
<div id="background">
    <div class="fit-container">
        <div class="center-container">
            <img id="fit" src={fit} alt="Shirt and Pants"/>
        </div>
    </div>
</div>
<div class="center-container">
    {#if $navigating}
        <Loading/>
    {:else}
        <slot/>
    {/if}
</div>