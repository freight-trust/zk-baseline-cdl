template over18() {
  signal input hash;
  signal private input age;
  signal output oldEnough;

  oldEnough <-- age >= 18 ? 1 : 0;
  oldEnough === 1;
}

component main = over18();