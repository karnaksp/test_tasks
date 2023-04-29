
preparatA <- c(48, 52, 55, 39, 60, 57, 46, 53, 50, 45, 63, 51, 40, 37, 44)
preparatB <- c(42, 46, 39, 35, 52, 49, 38, 41, 47, 36, 54, 50, 33, 30, 43)
t.test(preparatA, preparatB, alternative = "two.sided", var.equal = TRUE, conf.level = 0.95)
