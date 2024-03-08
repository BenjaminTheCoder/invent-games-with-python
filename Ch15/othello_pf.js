const R = require("ramda");
const prompt = require("prompt-sync")({ sigint: true });
const assert = require("assert");
const seedrandom = require("seedrandom");

// Helpers
const trace = R.curry((message, x) => {
  console.log(message, x);
  return x;
});

const pipe_ = (...fns) =>
  fns.reduce(
    (f, g) => (x) => g(f(x)),
    (x) => x
  );

const juxt_ =
  (...fns) =>
  (x) =>
    fns.map((f) => f(x));

const apply_ = (f) => (args) => f(...args);
//const func = (name, args, impl) => R.apply(impl(args));

const converge_ = (fns, f) => pipe_(juxt_(...fns), apply_(f));

//https://github.com/pdme/compound
//https://stackoverflow.com/a/46486941/3512820
const compound =
  (...fns) =>
  (...args) =>
    fns.reduce((result, fn) => fn(...[result, ...args.slice(1)]), args[0]);

// https://gist.github.com/Avaq/1f0636ec5c8d6aed2e45
const I = (x) => x;
const K = R.curry((x, y) => x);
const A = R.curry((f, x) => f(x));
const T = R.curry((x, f) => f(x));
const W = R.curry((f, x) => f(x, x));
const C = R.curry((f, y, x) => f(x, y));
const B = R.curry((f, g, x) => f(g(x)));
const B_ = R.curry((f, g, x) => g(f(x)));
const B2 = R.curry((f, g, x, y) => f(g(x, y), y));
const B2_ = R.curry((f, g, x, y) => g(f(x, y), y));
const S = R.curry((f, g, x) => f(x, g(x)));
const S_ = R.curry((f, g, x) => f(g(x), x));
const S2 = R.curry((f, g, h, x) => f(g(x), h(x)));
const P = R.curry((f, g, x, y) => f(g(x), g(y)));
const P2 = R.curry((f, g, h, x, y) => f(g(x), h(y)));
const Y = (f) => ((g) => g(g))((g) => f((x) => g(g)(x)));

// Here we go
const X_X = R.curry((x) => x);
const XY_X = R.curry((x, y) => x);
const XY_Y = R.curry((x, y) => y);
const FX_FX = R.curry((f, x) => f(x));
const XF_FX = R.curry((x, f) => f(x));
const FX_FXX = R.curry((f, x) => f(x, x));
const XF_FXX = R.curry((x, f) => f(x, x));
const FX_FFX = R.curry((f, x) => f(f(x)));
const XF_FFX = R.curry((x, f) => f(f(x)));
const FXY_FXY = R.curry((f, x, y) => f(x, y));
const FXY_FYX = R.curry((f, x, y) => f(y, x));

const label = R.curry((label, x) => x);

const promptFunc = R.curry((message, x) => prompt(message));

const grid = R.curry((w, h, x) => R.repeat(R.repeat(x, w), h));

const surroundWith = converge_([R.prepend, R.append], pipe_);
//const surroundWith = pipe_(juxt_(R.prepend, R.append), R.apply(pipe_));
//const surroundWith = (elem) => R.pipe(R.prepend(elem), R.append(elem));
//const surroundWith = R.pipe(R.unapply(R.ap([R.prepend, R.append])), R.apply(R.pipe));
//const surroundWith = R.converge(R.apply(R.pipe), [R.unapply(R.ap([R.prepend, R.append]))]);

const doesNotEqual = R.complement(R.equals);
const doesNotContain = R.complement(R.contains);

// Source: https://stackoverflow.com/a/24336780/3512820
const randomChoice = R.curry((rng, arr) => arr[Math.floor(arr.length * rng())]);

// Source: https://stackoverflow.com/a/35705266/3512820
const permutations = R.compose(R.sequence(R.of), R.flip(R.repeat));

const setLensPaths = R.curry((val, paths, obj) =>
  R.apply(
    R.pipe,
    R.map((path) => R.set(R.lensPath(path), val), paths)
  )(obj)
);

const toggle = R.curry((option1, option2, currentOption) =>
  currentOption === option1 ? option2 : option1
);

// Program
const newBoard = pipe_(
  K(grid(8, 8, "·")),
  setLensPaths("X", [
    [3, 3],
    [4, 4],
  ]),
  setLensPaths("O", [
    [3, 4],
    [4, 3],
  ])
);

const getBoardString = (board) =>
  R.pipe(
    surroundWith(["a", "b", "c", "d", "e", "f", "g", "h"]),
    R.transpose,
    surroundWith(R.map(R.toString, R.range(0, 10))),
    R.transpose,
    setLensPaths(" ", permutations(2, [0, 9])),
    R.map(R.join(" ")),
    R.join("\n")
  )(board);

// TODO Add ability to pass
const parseUserInput = pipe_(
  R.trim,
  R.toLower,
  R.cond([
    [pipe_(R.length, doesNotEqual(2)), K("Input must be of length 2.")],
    [pipe_(R.head, R.flip(doesNotContain)("abcdefgh")), K("First character must be in abcdefgh.")],
    [pipe_(R.last, R.flip(doesNotContain)("12345678")), K("Second character must be in 12345678.")],
    [R.T, (str) => [R.indexOf(str[1], "12345678"), R.indexOf(str[0], "abcdefgh")]],
    //[R.T, R.juxt([R.pipe(R.last, R.flip(R.indexOf)("12345678")), R.pipe(R.head, R.flip(R.indexOf)("abcdefgh"))])],
  ])
);

const getUserInput = (prompt) =>
  R.until(
    R.is(Array),
    pipe_(promptFunc(prompt), parseUserInput, R.when(R.is(String), trace("Input error: ")))
  )(prompt);

//const viewSpace = pipe_(juxt_(pipe_(R.nth(0), R.lensPath), R.nth(1)), R.apply(R.view));
//const viewSpace = R.curryN(2, converge_([pipe_(R.nthArg(0), R.lensPath), R.nthArg(1)], R.view));
//const viewSpace = R.curry((space, board) => R.view(R.lensPath(space), board));
//const viewSpace = R.useWith((space, board) => [space, board], [R.identity, R.identity]);
//const viewSpace = compound(R.lensPath, R.view);
const getSpace = (coords, board) => R.path(coords, board);

//const isSpaceAvailable = R.curry((coords, board) => viewSpace(coords, board) === "·");
const isSpaceAvailable = (coords, board) => R.pipe(getSpace, R.equals("·"))(coords, board);

const newGameState = (rng) => {
  return {
    whoseTurn: randomChoice(rng, ["X", "O"]),
    board: newBoard(),
    scoreX: 2, //TODO Compute this
    scoreO: 2, //TODO Compute this
    gameOver: false, //TODO Compute this
    rng: rng,
  };
};

const getGameStateString = pipe_(
  juxt_(
    pipe_(R.prop("board"), getBoardString),
    K("    Score X: "),
    pipe_(R.prop("scoreX"), String),
    K(" | O: "),
    pipe_(R.prop("scoreO"), String)
  ),
  R.join("")
);

const isValidMove = (move, gameState) =>
  R.cond([
    [R.useWith(R.complement(isSpaceAvailable), [I, R.prop("board")]), K("Space is occupied.")],
    [R.pipe(getTilesToFlip, R.length, R.equals(1)), K("Must flip at least one tile.")],
    [R.T, K(true)],
  ])(move, gameState);

// const stopTraversing = R.curry(
//   (whoseTurn, space) => space === "·" || space === whoseTurn || space === undefined
// );
// const stopTraversing = R.anyPass([R.flip(R.equals("·")), R.equals, R.flip(R.isNil)]);
const stopTraversing = (whoseTurn, space) =>
  R.anyPass([R.flip(R.equals("·")), R.equals, R.flip(R.isNil)])(whoseTurn, space);

const traverseInDirection = (start, dir, gameState, tilesToFlip) => {
  const nextSpaceCoords = R.zipWith(R.add, start, dir);
  tilesToFlip = R.append(nextSpaceCoords, tilesToFlip);
  const space = getSpace(nextSpaceCoords, gameState.board);
  return stopTraversing(gameState.whoseTurn, space)
    ? gameState.whoseTurn === space
      ? R.init(tilesToFlip)
      : []
    : traverseInDirection(nextSpaceCoords, dir, gameState, tilesToFlip);
};

const getTilesToFlip = (start, gameState) =>
  R.prepend(
    start,
    R.chain(
      (dir) => traverseInDirection(start, dir, gameState, []),
      R.without([[0, 0]], permutations(2, [0, 1, -1]))
    )
  );

// const flipTiles = (tilesToFlip, gameState) =>
//   R.useWith(setLensPaths(gameState.whoseTurn), [R.map(R.prepend("board")), I])(
//     tilesToFlip,
//     gameState
//   );

// const flipTiles = R.curry((tilesToFlip, gameState) =>
//   setLensPaths(gameState.whoseTurn, R.map(R.prepend("board"), tilesToFlip), gameState)
// );

const flipTiles = R.curry((tilesToFlip, gameState) =>
  R.pipe(
    R.juxt([R.pipe(R.nthArg(1), R.prop("whoseTurn")), R.map(R.prepend("board")), R.nthArg(1)]),
    R.apply(setLensPaths)
  )(tilesToFlip, gameState)
);

// const flipTiles = R.curry((tilesToFlip, gameState) =>
//   R.converge(setLensPaths, [
//     R.pipe(R.nthArg(1), R.prop("whoseTurn")),
//     R.map(R.prepend("board")),
//     R.nthArg(1),
//   ])(tilesToFlip, gameState)
// );

// const makeMove = R.curry((move, gameState) =>
//   R.pipe(
//     R.juxt([getTilesToFlip, R.nthArg(1)]),
//     R.apply(flipTiles),
//     R.over(R.lensPath(["whoseTurn"]), toggle("X", "O"))
//   )(move, gameState)
// );

const makeMove = R.curry((move, gameState) =>
  R.pipe(
    compound(getTilesToFlip, flipTiles), //
    R.over(R.lensPath(["whoseTurn"]), toggle("X", "O"))
  )(move, gameState)
);

// const makeMove = R.curry((move, gameState) =>
//   R.pipe(
//     R.curry((f, g, x, y) => g(f(x, y), y))(getTilesToFlip, flipTiles), // Inline combinator
//     R.over(R.lensPath(["whoseTurn"]), toggle("X", "O"))
//   )(move, gameState)
// );

// const makeMove = R.pipe(
//   R.juxt([getTilesToFlip, R.nthArg(1)]),
//   R.apply(flipTiles),
//   R.over(R.lensPath(["whoseTurn"]), toggle("X", "O"))
// );

const isGameOver = (gameState) => gameState.gameOver === true;

const gameLoop = (gameState) => {
  while (!isGameOver(gameState)) {
    console.log(`\n${getGameStateString(gameState)}\n`);
    const move = getUserInput(`Enter move for ${gameState.whoseTurn}: `);
    const validMove = isValidMove(move, gameState);
    if (R.is(String, validMove)) {
      console.log(`\nInvalid move: ${validMove}`);
      gameLoop(gameState);
    }
    gameLoop(makeMove(move, gameState));
  }
};

// Tests
console.log(getBoardString(newBoard()));

assert.deepStrictEqual(parseUserInput("d6"), [5, 3]);

//console.log(getUserInput("Enter your move: "));

assert.deepStrictEqual(getSpace([3, 3], newBoard()), "X");
assert.deepStrictEqual(isSpaceAvailable([0, 3], newBoard()), true);
assert.deepStrictEqual(isSpaceAvailable([3, 3], newBoard()), false);

const seed = "1234";

console.log(getGameStateString(newGameState(seedrandom(seed))));
assert.deepStrictEqual(isValidMove([3, 3], newGameState(seedrandom(seed))), "Space is occupied.");
assert.deepStrictEqual(
  isValidMove([0, 0], newGameState(seedrandom(seed))),
  "Must flip at least one tile."
);
assert.deepStrictEqual(isValidMove([5, 3], newGameState(seedrandom(seed))), true);

assert.deepStrictEqual(stopTraversing("X", "O"), false);
assert.deepStrictEqual(stopTraversing("X", "X"), true);
assert.deepStrictEqual(stopTraversing("X", undefined), true);
assert.deepStrictEqual(stopTraversing("X", "·"), true);
assert.deepStrictEqual(traverseInDirection([5, 3], [-1, 0], newGameState(seedrandom(seed)), []), [
  [4, 3],
]);
assert.deepStrictEqual(getTilesToFlip([5, 3], newGameState(seedrandom(seed))), [
  [5, 3],
  [4, 3],
]);
assert.deepStrictEqual(getTilesToFlip([2, 4], newGameState(seedrandom(seed))), [
  [2, 4],
  [3, 4],
]);

console.log(getGameStateString(makeMove([5, 3], newGameState(seedrandom(seed)))));
console.log(getGameStateString(makeMove([3, 2], makeMove([5, 3], newGameState(seedrandom(seed))))));
// gameLoop(newGameState(seedrandom(seed)));
