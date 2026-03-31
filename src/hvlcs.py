def hvlcs(values, A, B):
    """
    2. Compute the maximum value of a common subsequence
    3. Reconstruct one optimal subsequence
    4. Output both the value and the subsequence

    dp[i][j] stores the maximum value of a common subsequence between A[i:] and B[j:]
    Extra row and column are for base cases, where one of the strings is empty. In that case, the value is 0
    """
    # Get lengths of the two strings
    n = len(A) 
    m = len(B)

    # Initialize DP table with zeros
    dp = [[0] * (m + 1) for i in range(n + 1)]

    # Fill table bottom-up (from the end of the strings to the beginning)
    for i in range(n - 1, -1, -1):  # Iterate backwards through A
        for j in range(m - 1, -1, -1):  # Iterate backwards through B

            # Case 1a: Skip A[i]
            # Case 1b: Skip B[j]
            # Take the better of the two
            best = max(dp[i + 1][j], dp[i][j + 1])
            
            # Case 2: A[i] and B[j] characters match
            # Include value of A[i] (which is the same as B[j]) and add it to the maximum from remaining suffixes
            if A[i] == B[j]:
                best = max(best, values[A[i]] + dp[i + 1][j + 1])
            
            # Store result in DP table
            dp[i][j] = best

    # Reconstruct one optimal subsequence
    i, j = 0, 0
    solution = []

    # Follow optimal choices in DP table to reconstruct the subsequence
    while i < n and j < m:

        # If characters match AND using them gives optimal value, include the character in the solution
        if A[i] == B[j] and dp[i][j] == values[A[i]] + dp[i + 1][j + 1]:
            solution.append(A[i])
            i += 1
            j += 1
        
        # Otherwise, move in the direction that gave the optimal value
        elif dp[i][j] == dp[i + 1][j]:
            i += 1  # Skipped A[i]
        else:
            j += 1  # Skipped B[j]

    # dp[0][0] = Maximum value
    return dp[0][0], "".join(solution)