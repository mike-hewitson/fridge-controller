var express = require('express');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');

var Readings = require('../models/readings');

var readingRouter = express.Router();

readingRouter.use(bodyParser.json());

readingRouter.route('/')
    .get(function(req, res, next) {
        Readings.find({}, function(err, reading) {
            if (err) throw err;
            res.json(reading);
        });
    })
    .post(function(req, res, next) {
        Readings.create(req.body, function(err, reading) {
            if (err) throw err;
            console.log('reading created!');
            var id = reading._id;

            res.writeHead(200, {
                'Content-Type': 'text/plain'
            });
            res.end('Added the reading with id: ' + id);
        });
    })
    .delete(function(req, res, next) {
        Readings.remove({}, function(err, resp) {
            if (err) throw err;
            res.json(resp);
        });
    });

readingRouter.route('/latest')
    .get(function(req, res, next) {
        var query = Readings.find().limit(1).sort({ $natural: -1 });
        query.exec(function(err, reading) {
            if (err) throw err;
            res.json(reading);
        });
    });

readingRouter.route('/:readingId')
    .get(function(req, res, next) {
        Readings.findById(req.params.readingId, function(err, reading) {
            if (err) throw err;
            res.json(reading);
        });
    })
    .put(function(req, res, next) {
        Readings.findByIdAndUpdate(req.params.readingId, {
            $set: req.body
        }, {
            new: true
        }, function(err, reading) {
            if (err) throw err;
            res.json(reading);
        });
    })
    .delete(function(req, res, next) {
        Readings.findByIdAndRemove(req.params.readingId, function(err, resp) {
            if (err) throw err;
            res.json(resp);
        });
    });

readingRouter.route('/:readingId/sensors')
    .get(function(req, res, next) {
        Readings.findById(req.params.readingId, function(err, reading) {
            if (err) throw err;
            res.json(reading.sensors);
        });
    })
    .post(function(req, res, next) {
        Readings.findById(req.params.readingId, function(err, reading) {
            if (err) throw err;
            reading.sensors.push(req.body);
            reading.save(function(err, reading) {
                if (err) throw err;
                console.log('Updated sensors!');
                res.json(reading);
            });
        });
    })
    .delete(function(req, res, next) {
        Readings.findById(req.params.readingId, function(err, reading) {
            if (err) throw err;
            for (var i = (reading.sensors.length - 1); i >= 0; i--) {
                reading.sensors.id(reading.sensors[i]._id).remove();
            }
            reading.save(function(err, result) {
                if (err) throw err;
                res.writeHead(200, {
                    'Content-Type': 'text/plain'
                });
                res.end('Deleted all sensors!');
            });
        });
    });

readingRouter.route('/:readingId/comments/:commentId')
    .get(function(req, res, next) {
        Readings.findById(req.params.readingId, function(err, reading) {
            if (err) throw err;
            res.json(reading.comments.id(req.params.commentId));
        });
    })
    .put(function(req, res, next) {
        // We delete the existing commment and insert the updated
        // comment as a new comment
        Readings.findById(req.params.readingId, function(err, reading) {
            if (err) throw err;
            reading.comments.id(req.params.commentId).remove();
            reading.comments.push(req.body);
            reading.save(function(err, reading) {
                if (err) throw err;
                console.log('Updated Comments!');
                res.json(reading);
            });
        });
    })
    .delete(function(req, res, next) {
        Readings.findById(req.params.readingId, function(err, reading) {
            reading.comments.id(req.params.commentId).remove();
            reading.save(function(err, resp) {
                if (err) throw err;
                res.json(resp);
            });
        });
    });

module.exports = readingRouter;
