/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F4F5F7",
        surface: "#FFFFFF",
        ink: "#16213C",
        muted: "#5B6472",
        hairline: "rgba(22, 33, 60, 0.10)",
        marigold: {
          DEFAULT: "#D98E04",
          dark: "#B57603",
          soft: "#FBEFD8",
        },
        teal: {
          DEFAULT: "#0E6E62",
          soft: "#E3F1EE",
        },
        danger: "#C0374A",
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        sans: ["Inter", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "10px",
      },
      maxWidth: {
        content: "1180px",
      },
      boxShadow: {
        panel: "0 1px 2px rgba(22,33,60,0.04), 0 12px 32px rgba(22,33,60,0.08)",
      },
    },
  },
  plugins: [],
};
