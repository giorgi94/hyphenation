const tree = require('./tree')


function zip(x, y) {
    var z = []
    for(var i=0; i<Math.min(x.length, y.length); i++) {
        z.push([x[i], y[i]])
    }
    return z
}


var hyphenate_word = (word) => {
    if(word.length < 5) {
        return word
    }

    var work = '.' + word + '.'
    var points = Array.from(Array(work.length + 1), () => 0)
    for(var i=0; i<work.length; i++) {
        var t = tree
        for(var c of work.slice(i)) {
            if(c in t) {
                t = t[c]
                if(null in t) {
                    var p = t[null]
                    for(var j=0; j<p.length; j++) {
                        points[i+j] = Math.max(points[i+j], p[j])
                    }
                }
            }
            else {
                break
            }
        }
    }

    points[1] = points[2] = points[points.length-2] = points[points.length-3] = 0
    var pieces = ['']

    zip(word, points.slice(2)).forEach((val)=>{
        pieces[pieces.length-1] += val[0]
        if(val[1] % 2) {
            pieces.push('')
        }
    })

    return pieces
}


var sentence = 'დედაქალაქის'

console.log(hyphenate_word(sentence))