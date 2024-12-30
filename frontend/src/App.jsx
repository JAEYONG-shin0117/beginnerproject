import { ThemeProvider } from "styled-components";
import { theme } from "./styles/theme";
import GlobalStyle from "./styles/global";
import { RouterProvider } from "react-router-dom";
import { router } from "./router";

const App = () => { // 함수 선언 그대로 유지
    return (
        <ThemeProvider theme={theme}>
            <GlobalStyle />
            <RouterProvider router={router} />
        </ThemeProvider>
    );
};

export default App; // 기본 내보내기
