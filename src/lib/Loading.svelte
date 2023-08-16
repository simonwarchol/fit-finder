<style>

    .loading {
        display: flex;
        flex-direction: row;
        margin-bottom: 17vh;
    }

    .loading__letter {
        font-size: 88px;
        font-weight: normal;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-family: 'Knewave', cursive;
        color: #FF5A5F;
        animation-name: bounce;
        animation-duration: 2s;
        animation-iteration-count: infinite;
    }

    .loading__letter:nth-child(2) {
        animation-delay: .1s;
    }

    .loading__letter:nth-child(3) {
        animation-delay: .2s;
    }

    .loading__letter:nth-child(4) {
        animation-delay: .3s;
    }

    .loading__letter:nth-child(5) {
        animation-delay: .4s;
    }

    .loading__letter:nth-child(6) {
        animation-delay: .5s;
    }

    .loading__letter:nth-child(7) {
        animation-delay: .6s;
    }

    .loading__letter:nth-child(8) {
        animation-delay: .8s;
    }

    .loading__letter:nth-child(9) {
        animation-delay: 1s;
    }

    .loading__letter:nth-child(10) {
        animation-delay: 1.2s;
    }

    @keyframes bounce {
        0% {
            transform: translateY(0px)
        }
        40% {
            transform: translateY(-40px);
        }
        80%,
        100% {
            transform: translateY(0px);
        }
    }


    @media (max-width: 700px) {
        .loading__letter {
            font-size: 50px;
        }
    }

    @media (max-width: 340px) {
        .loading__letter {
            font-size: 40px;
        }
    }
</style>
<div class="container">
    <div class="loading">
        <div class="loading__letter">L</div>
        <div class="loading__letter">o</div>
        <div class="loading__letter">a</div>
        <div class="loading__letter">d</div>
        <div class="loading__letter">i</div>
        <div class="loading__letter">n</div>
        <div class="loading__letter">g</div>
        <div class="loading__letter">.</div>
        <div class="loading__letter">.</div>
        <div class="loading__letter">.</div>
    </div>
</div>