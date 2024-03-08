//http://evincarofautumn.blogspot.com/2012/02/why-concatenative-programming-matters.html

//f x y z = y2 + x2 − |y|
//square = dup ×
//f = drop [square] [abs] bi − [square] dip +
const square = (x) => x * x;
const f = R.pipe(
  Array,
  R.juxt([R.pipe(R.take(2), R.map(square), R.sum), R.pipe(R.nth(1), Math.abs)]),
  R.apply(R.subtract)
)(2, 4, 5);
