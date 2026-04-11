module.exports = {
        proxy: "localhost:8000", // Your Django development server
        files: [
                // Watch these files for changes
                "./templates/**/*.html",
                "./static/**/*.css",
                "./static/**/*.js",
                "./**/*.py",
                "!./venv/**/*", // Ignore virtual environment
                "!./.git/**/*", // Ignore git directory
        ],
        reloadDelay: 1000,
        notify: false,
        open: false,
        port: 3000, // BrowserSync will run on port 3000
};
