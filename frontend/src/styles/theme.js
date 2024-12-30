const fontGenerator = (
    fontFamily,
    fontSize = "1rem",
    fontWeight = "400",
    lineHeight = "1.5",
    letterSpacing = "normal"
  ) => ({
    "font-family": fontFamily,
    "font-size": fontSize,
    "font-weight": fontWeight,
    "line-height": lineHeight,
    "letter-spacing": letterSpacing,
  });
  
  export const theme = {
    colors: {
      white: "#FFFFFF",
      default: "#000000",
      subText: "#5A5A5A",
      buttonPrimary: "#FF6601",
    },
  
    fonts: {
      default: fontGenerator("NanumSquareRoundR"),
      NanumSquareRoundR: fontGenerator("NanumSquareRoundR"),
    },
  };
  