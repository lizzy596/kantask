const express = require('express');
const auth = require('../../middlewares/auth');
const devController = require('../../controllers/dev.controller');

const router = express.Router();



router
  .route('/')
  .post(devController.createDev)
  .get(devController.getDevs);


router
  .route('/:devId')
  .get(devController.getDev)
  .patch(devController.updateDev)
  .delete(devController.deleteDev);

module.exports = router;
