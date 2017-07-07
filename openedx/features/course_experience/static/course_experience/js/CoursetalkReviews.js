/*
  Enable users to switch between viewing and writing CourseTalk reviews.
 */

export class CourseTalkReviews {  // eslint-disable-line import/prefer-default-export
  constructor() {
    const $courseTalkToggleReadWriteReviews = $('.toggle-read-write-reviews');

    const readSrc = '//d3q6qq2zt8nhwv.cloudfront.net/s/js/widgets/coursetalk-read-reviews.js';
    const writeSrc = '//d3q6qq2zt8nhwv.cloudfront.net/s/js/widgets/coursetalk-write-reviews.js';

    const toReadBtnText = 'View Reviews';
    const toWriteBtnText = 'Write a Review';

    // Initialize page to the read reviews view
    var currentSrc = readSrc;
    $courseTalkToggleReadWriteReviews.text(writeBtnText);

    $coursetalkToggleReadWriteReviews.on('click', () => {
      // Cache js file for future button clicks
      $.ajaxSetup({ cache: true });

      // Toggle the new coursetalk script object
      const switchToReadView = currentSrc === writeSrc;
      const newSource = switchToReadView ? readSrc : writeSrc;
      $.getScript(newSource);

      // Toggle button text on switch to the other view
      const newText = switchToReadView ? toWriteBtnText : toReadBtnText;
      $courseTalkToggleReadWriteReviews.text(newText);
    });
  }
}
