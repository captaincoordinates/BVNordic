@easy: #72ca61;
@intermediate: #1b7bc4;
@advanced: #000000;

#trails {
  line-width: 10;
  line-smooth: .3;
  [closed = 1] {
    line-color: #A9A9A9;
    line-dasharray: 30, 10;
  }
  [lit = 1] {
    ::case {
      line-width: 16;
      line-color: #FFFF00;
    }
  }
}

#trails {
  [closed = 0] {
    [difficulty = 'easy'] {
      line-color: @easy;
    }
    [difficulty = 'intermediate'] {
      line-color: @intermediate;
    }
    [difficulty = 'advanced'] {
      line-color: @advanced;
    }
    [lit = 1] {
      ::fill {
        line-width: 10;
        [difficulty = 'easy'] {
          line-color: @easy;
        }
        [difficulty = 'intermediate'] {
          line-color: @intermediate;
        }
        [difficulty = 'advanced'] {
          line-color: @advanced;
        }
      }
    }
  }
}

#background {
  polygon-fill: rgba(255, 255, 255, 0.6);
}