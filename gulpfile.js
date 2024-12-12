var gulp = require('gulp');
var del = require('del');
var runSequence = require('run-sequence');
var browserSync = require('browser-sync').create();
var sass = require('gulp-sass');
var ejs = require('gulp-ejs');
var header = require('gulp-header');
var replace = require('gulp-replace');
var sourcemaps = require('gulp-sourcemaps');
var plumber = require('gulp-plumber');
var notify = require('gulp-notify');
var postcss = require('gulp-postcss');
var autoprefixer = require('autoprefixer');
var assets  = require('postcss-assets');
var cssdeclsort = require('css-declaration-sorter');
var mqpacker = require('css-mqpacker');
var csso = require('gulp-csso');
var imagemin = require('gulp-imagemin');
var pngquant  = require('imagemin-pngquant');
var mozjpeg  = require('imagemin-mozjpeg');
var changed = require('gulp-changed');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');

var paths = {
  'templates': ['./_src/templates/**/*.ejs'],
  'scssSrc' : './_src/assets/scss/**/*.scss',
  'jsSrc'   : './_src/assets/js/**/*.js',
  'imgSrc'  : './_src/assets/images/**/*.{png,jpg,gif,svg,ico}',
  'imgDir'  : './dist/assets/images/',
  'rootDir' : './dist/'
};

gulp.task('clean', () => {
  return del(['dist/**']).then(function() {
    console.log('dist directory was cleaned');
    return gulp;
  });
});

gulp.task('ejs', () => {

  gulp.src(paths.templates)
    .pipe(plumber({
      handleError: (err) => {
        console.log(err);
        this.emit('end');
      }
    }))
    .pipe(ejs({}, {}, {ext: '.html'}))
    .pipe(gulp.dest(paths.rootDir));

});

gulp.task('scss', () => {
  return gulp.src(paths.scssSrc)
    .pipe(plumber({errorHandler: notify.onError("Error: <%= error.message %>")}))
    .pipe(sourcemaps.init())
    .pipe(sass({outputStyle: 'expanded'}))
    .pipe(replace(/@charset "UTF-8";/g, ''))
    .pipe(header('@charset "UTF-8";\n\n'))
    .pipe(postcss([mqpacker({sort: true})]))
    .pipe(postcss([cssdeclsort({order: 'concentric-css'})]))
    .pipe(postcss([assets({
      loadPaths: ['/images/common', '/images/top'], relative: true})]))
    .pipe(postcss([autoprefixer({browsers: ['last 1 versions', 'ie 10']})]))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.rootDir + '/assets/css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(csso())
    .pipe(gulp.dest(paths.rootDir + '/assets/css'));
});

gulp.task('image', () => {
  return gulp.src(paths.imgSrc)
    .pipe(changed(paths.imgDir))
    .pipe(imagemin([
       pngquant({
         quality: '65-80',
         speed: 1,
         floyd:0
       }),
       mozjpeg({
         quality:85,
         progressive: true
       }),
       imagemin.svgo(),
       imagemin.optipng(),
       imagemin.gifsicle()
     ]))
    .pipe(imagemin()) //余計なガンマ情報を削除してMacの減色で暗くならないようにする
    .pipe(gulp.dest(paths.imgDir));
});

gulp.task('js', () => {
  return gulp.src(paths.jsSrc)
    .pipe(uglify({
      output:{
        comments: /^!/
      }
    }))
    .pipe(rename({
      extname: '.min.js'
    }))
    .pipe(gulp.dest(paths.rootDir + '/assets/js'));
});

gulp.task('webserver', () => {
  browserSync.init({
    server: {
      baseDir: "dist",
      index: "index.html"
    }
  })
});

gulp.task('bs-reload', () => {
  browserSync.reload();
});

gulp.task('watch', ['default'], () => {
  gulp.watch([paths.templates], ['ejs', 'bs-reload']);
  gulp.watch([paths.scssSrc], ['scss', 'bs-reload']);
  gulp.watch([paths.imgSrc], ['image', 'bs-reload']);
  gulp.watch([paths.jsSrc], ['js', 'bs-reload']);
});

gulp.task('default', (callback) => {
  return runSequence(
    'clean',
    ['ejs', 'image', 'js', 'scss', 'webserver'],
    callback
  )
});