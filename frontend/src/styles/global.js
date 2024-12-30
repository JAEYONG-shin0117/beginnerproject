import { createGlobalStyle } from "styled-components";

const GlobalStyle = createGlobalStyle`
    :root {
        --vh: 100%;
        --font-family: 'Pretendard-Regular';
    }

    /* 폰트 페이스 추가 */
    @font-face {
        font-family: 'Pretendard-Thin';
        src: url('https://cdn.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Thin.woff') format('woff');
        font-weight: 100;
        font-style: normal;
    }
    @font-face {
        font-family: 'Pretendard-Regular';
        src: url('https://cdn.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Regular.woff') format('woff');
        font-weight: 400;
        font-style: normal;
    }
    @font-face {
        font-family: 'Pretendard-Bold';
        src: url('https://cdn.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Bold.woff') format('woff');
        font-weight: 700;
        font-style: normal;
    }

    /* 기본 스타일 초기화 */
    html, body, div, span, applet, object, iframe,
    h1, h2, h3, h4, h5, h6, p, blockquote,
    a, abbr, acronym, address, big, cite,
    del, em, strong, dfn, img, ins, kbd, q, s, samp,
    small, strike, sub, sup, tt, var,
    b, u, i, center,
    dl, dt, dd, menu, ol, ul, li,
    fieldset, form, label, legend,
    table, caption, tbody, tfoot, thead, tr, th, td,
    article, aside, canvas, details, embed,
    figure, figcaption, footer, header, hgroup,
    main, menu, nav, output, ruby, section, summary,
    time, mark, audio, video {
        margin: 0;
        border: 0;
        padding: 0;
        vertical-align: baseline;
    }

    article, aside, details, figcaption, figure,
    footer, header, hgroup, main, menu, nav, section {
        display: block;
    }

    *[hidden] {
        display: none;
    }

    body {
        touch-action: manipulation;
        font-family: var(--font-family);
        //background-color: #000000;     색상은 미정
        //color: #111111;
        margin: 0 auto;
        max-width: 430px; /* 모바일 뷰에서 최대 너비 제한 */
        min-height: 100vh;
        overflow-x: hidden;
    }

    menu, ol, ul {
        list-style: none;
    }

    blockquote, q {
        quotes: none;
    }

    blockquote:before, blockquote:after,
    q:before, q:after {
        content: '';
        content: none;
    }

    table {
        border-collapse: collapse;
        border-spacing: 0;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    #root {
        width: 100%;
        max-width: 430px; /* 모바일 뷰에서 최대 너비 제한 */
        margin: 0 auto;
        padding: 0 ; /* 양쪽 여백 */
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    html {
        font-family: var(--font-family);
        -webkit-touch-callout: none;
        //-webkit-tap-highlight-color: rgba(0, 0, 0, 0);   #색상은 미정이므로 주석처리
        scroll-behavior: smooth;
        font-size: 100%;
    }

    /* 반응형 폰트 크기 설정 */
    @media screen and (max-width: 1799px) {
        html {
            font-size: 50%;
        }
    }
    @media screen and (max-width: 1199px) {
        html {
            font-size: 45%;
        }
    }
    @media screen and (max-width: 991px) {
        html {
            font-size: 40%;
        }
    }
    @media screen and (max-width: 767px) {
        html {
            font-size: 30%;
        }
    }

    ul, li {
        padding-left: 0rem;
        list-style: none;
    }

    a {
        text-decoration: none;
        color: inherit;
    }

    input, button {
        outline: none;
        border: none;
        background-color: transparent;
    }

    button {
        cursor: pointer;
        padding: 0;
    }

    input {
        appearance: none;

        &:focus {
            outline: none;
        }
    }

    select {
        border: none;

        &:focus {
            outline: none;
        }
    }

    .scroll::-webkit-scrollbar {
        display: none;
    }

    .scroll {
        -ms-overflow-style: none; /* 인터넷 익스플로러 */
        scrollbar-width: none; /* 파이어폭스 */
    }
`;

export default GlobalStyle;
