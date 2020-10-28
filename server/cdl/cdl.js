$(document).ready(function () {
  $(".cdl") /// VALID
    .delay(2000)
    .animate(
      {
        height: "360px",
      },
      1500
    )
    .delay(1600)
    .slideUp(500);

  $("#validation") // CLASSIFCATION
    .delay(3400)
    .animate(
      {
        height: "170px",
      },
      2500
    );

  $(".CDL-VALID") // TSA CHECK
    .delay(3400)
    .animate(
      {
        bottom: "200px",
      },
      2500
    );
});
