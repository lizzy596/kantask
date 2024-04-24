const mongoose = require('mongoose');
const { toJSON, paginate } = require('./plugins');

const devSchema = mongoose.Schema(
  {
    test: {
      type: Number,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

// add plugin that converts mongoose to json
devSchema.plugin(toJSON);
devSchema.plugin(paginate);



devSchema.statics.searchableFields = function () {
  return ['category'];
};

const Dev = mongoose.model('Dev', devSchema);

module.exports = Dev;


