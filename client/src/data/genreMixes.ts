/**
 * Hardcoded genre mixes, ported from the Jinja templates
 * x_by_genre.html and x_by_year_range_and_genre.html.
 */

export interface GenreMix {
  genres: string[]
}

export interface YearRangeGenreMix {
  minYear: number
  maxYear: number
  genres: string[]
  /**
   * When true, the year range is ignored (matches the "90s Metal Mix" entry in
   * x_by_year_range_and_genre.html, which includes x_by_genre_tr.html).
   */
  genreOnly?: boolean
}

/** From x_by_genre.html */
export const GENRE_MIXES: GenreMix[] = [
  { genres: ['Classic Rock'] },
  { genres: ['Indie Rock'] },
  { genres: ['Alternative Rock'] },
  { genres: ['Indie Folk'] },
  { genres: ['Alternative Metal'] },
  // Hip-Hop Mix
  { genres: ['Hip-Hop', 'Hip-Hop français', 'Hip-Hop/Electronic', 'Hip-Hop/Reggae', 'Trip hop', 'Urbano'] },
  // Emo mix
  { genres: ['Post-Hardcore', 'Emo / Pop-Rock'] },
  // Rock around the world Mix
  { genres: ['Rock français', 'Rock brasileiro', 'Rock en español', 'Korean Rock', 'Japanese Rock', 'Zamrock'] },
  // Funk Rock/Metal Mix
  { genres: ['Funk Metal', 'Funk Rock'] },
  // Alternative Metal Mix (Excluding 'Alternative Rock')
  { genres: ['Alternative Metal', 'Grunge', 'Sludge Metal', 'Stoner Rock'] },
  // Alternative Soft Rock Mix (Excluding 'Alternative Rock')
  { genres: ['Alternative', 'Shoegaze', 'Noise Rock'] },
  // Pop Mix
  { genres: ['Classic Pop', 'Britpop', 'Pop', 'Dream Pop', 'Pop Rock'] },
  // Soft Rock Mix
  { genres: ['Soft Rock', 'Easy Listening'] },
  // Psychedelic Rock Mix
  { genres: ['Psychedelic Rock', 'Blues Rock'] },
  // Classic Prog Mix
  { genres: ['Classic Prog'] },
  // Heavy Metal Mix
  { genres: ['Heavy Metal', 'Glam Metal'] },
  // Electronic Mix
  { genres: ['Electronic', 'Electronica', 'Electronic (Instrumental)', 'Dance/Electronic', 'Deep House', 'Trance', 'Techno', 'Eurodance'] },
  // Punk Mix
  { genres: ['Punk', 'Punk Rock', 'Horror Punk', 'Punk français', 'Ska Punk'] },
  // New Wave Mix
  { genres: ['New Wave', 'Synth-pop', 'New Wave français'] },
  // Goth Mix
  { genres: ['Post-Punk', 'Goth Rock'] },
  // RnB Mix
  { genres: ['R&B', 'R&B/Soul', 'R&B (Instrumental)', 'R&B/Funk', 'RnB français'] },
  // Latin Mix
  { genres: ['Latin', 'Cumbia', 'Merengue', 'Bachata', 'Salsa', 'Norteño', 'Latin Pop', 'Urbano', 'Latin Funk', 'Reggaeton', 'Rock en español', 'Rock brasileiro', 'Afrobeat'] },
  // Reggae Mix
  { genres: ['Reggae', 'Reggae Rock', 'Reggaeton', 'Ska Punk'] },
  // Metal Mix
  { genres: ['Black Metal', 'Death Metal', 'Doom Metal', 'Glam Metal', 'Heavy Metal', 'Industrial Metal', 'Nu Metal', 'Post-Black Metal', 'Post-Metal', 'Sludge Metal', 'Thrash Metal'] },
  // Industrial Mix
  { genres: ['Industrial Metal', 'Industrial', 'Post-Industrial'] },
  // Country Mix
  { genres: ['Classic Country', 'Country', 'Country Pop'] },
  // Prog Mix
  { genres: ['Progressive Metal', 'Progressive Pop'] },
  // Folk Mix
  { genres: ['Folk', 'Folk Pop', 'Folk Punk', 'Folk Rock', 'Folk rock, Jazz', 'Indie Folk', 'Psychedelic Folk'] },
  // Classic Funk Mix
  { genres: ['Funk'] },
  // Contemporary Funk Mix
  { genres: ['Funk', 'Funk (Instrumental)', 'Jazz/Funk', 'Latin Funk', 'R&B/Funk'] },
  // House Mix
  { genres: ['Deep House', 'French House', 'House'] },
  // Jazz Mix
  { genres: ['Dixieland Jazz', 'Jazz', 'Jazz/Pop', 'Jazz Rock', 'Nu Jazz', 'Nu Jazz (Instrumental)', 'Smooth Jazz'] },
  // Misc rock mix
  { genres: ['Acid Rock', 'Art Rock', 'Celtic Rock', 'Emo / Pop-Rock', 'Experimental Ambient Rock', 'Glam Rock', 'Goth Rock', 'Indie Rock', 'Japanese Rock', 'Korean Rock', 'Noise Rock', 'Pop Rock', 'Post-Grunge', 'Post-Hardcore', 'Post-Industrial', 'Post-Punk', 'Post-Rock', 'Prog Rock', 'Psychedelic Rock', 'Punk Rock', 'Reggae Rock', 'Rock brasileiro', 'Rock en español', 'Rock italiano', 'Soft Rock', 'Southern Punk Rock', 'Southern Rock', 'Stoner Rock'] },
  // Surf mix
  { genres: ['Surf Punk', 'Surf Rock'] },
  // French mix
  { genres: ['Hip-Hop français', 'Nu Metal français', 'Punk français', 'RnB français', 'Rock français'] },
  // Workout mix
  { genres: ['Industrial Metal', 'Punk', 'Punk Rock', 'Heavy Metal', 'Hip-Hop', 'Urbano', 'Thrash Metal', 'Nu Metal', 'Rock en español', 'Funk Metal', 'Hip-Hop français'] },
]

/**
 * From x_by_year_range_and_genre.html.
 * @param presentYear used in place of the Jinja PRESENT_YEAR global.
 */
export function getYearRangeGenreMixes(presentYear: number): YearRangeGenreMix[] {
  return [
    // 2015-present Hip-Hop Mix
    { minYear: 2015, maxYear: presentYear, genres: ['Hip-Hop', 'Hip-Hop français', 'Hip-Hop/Electronic', 'Hip-Hop/Reggae', 'Trip hop'] },
    // Late 90s to early 2000s Emo Mix
    { minYear: 1998, maxYear: 2008, genres: ['Post-Hardcore', 'Emo / Pop-Rock'] },
    // Mid 90s to early 2010s Indie Mix
    { minYear: 1995, maxYear: 2015, genres: ['Indie Rock'] },
    // Mid 90s to early 2010s Indie Folk Mix
    { minYear: 1995, maxYear: 2015, genres: ['Indie Folk'] },
    // Late 00s to mid 2010s Hip-Hop Mix
    { minYear: 2005, maxYear: 2014, genres: ['Hip-Hop'] },
    // Mid 90s and early 00s Pop Rock Mix
    { minYear: 1995, maxYear: 2004, genres: ['Pop Rock'] },
    // Mid 90s to early 00s Hip-Hop Mix
    { minYear: 1995, maxYear: 2004, genres: ['Hip-Hop'] },
    // 90s Metal Mix (genre-only link in the original template)
    { minYear: 1990, maxYear: 1999, genres: ['Black Metal', 'Death Metal', 'Doom Metal', 'Glam Metal', 'Heavy Metal', 'Industrial Metal', 'Nu Metal', 'Post-Black Metal', 'Post-Metal', 'Sludge Metal', 'Thrash Metal'], genreOnly: true },
    // 90s and early 2000s Alternative Metal Mix (Excluding 'Alternative Rock')
    { minYear: 1990, maxYear: 2004, genres: ['Alternative Metal'] },
    // Very late 80s and 90s Alternative Rock Mix
    { minYear: 1988, maxYear: 1999, genres: ['Alternative Rock'] },
    // Mid 80s and early 90s Hip-Hop Mix
    { minYear: 1985, maxYear: 1994, genres: ['Hip-Hop'] },
    // Late 80s to Early 90s Alternative Metal Mix (Excluding 'Alternative Rock')
    { minYear: 1985, maxYear: 1994, genres: ['Alternative Metal', 'Grunge', 'Sludge Metal', 'Stoner Rock'] },
    // 80s Metal Mix
    { minYear: 1980, maxYear: 1989, genres: ['Black Metal', 'Death Metal', 'Doom Metal', 'Glam Metal', 'Heavy Metal', 'Industrial Metal', 'Nu Metal', 'Post-Black Metal', 'Post-Metal', 'Sludge Metal', 'Thrash Metal'] },
    // Late 80s to Early 90s Funk Rock/Metal Mix
    { minYear: 1985, maxYear: 1994, genres: ['Funk Metal', 'Funk Rock'] },
    // Late 80s to Early 90s Country Mix
    { minYear: 1985, maxYear: 1994, genres: ['Classic Country', 'Country', 'Country Pop'] },
    // 80s Alternative Soft Rock Mix (Excluding 'Alternative Rock')
    { minYear: 1980, maxYear: 1989, genres: ['Alternative', 'Shoegaze', 'Noise Rock'] },
    // 80s Pop Mix
    { minYear: 1980, maxYear: 1989, genres: ['Classic Pop', 'Britpop', 'Pop', 'Dream Pop', 'Pop Rock'] },
    // 80s Classic Rock Mix
    { minYear: 1980, maxYear: 1989, genres: ['Classic Rock'] },
    // 80s Classic Prog Rock Mix
    { minYear: 1980, maxYear: 1989, genres: ['Classic Prog'] },
    // 80s Hair Metal Mix
    { minYear: 1980, maxYear: 1989, genres: ['Heavy Metal', 'Glam Metal'] },
    // Late 70s and 80s New Wave Mix
    { minYear: 1975, maxYear: 1989, genres: ['New Wave', 'Synth-pop', 'New Wave français'] },
    // Late 70s and 80s Electronic Mix
    { minYear: 1970, maxYear: 1989, genres: ['Electronic', 'Electronic (Instrumental)'] },
    // Late 70s and 80s Punk Mix
    { minYear: 1975, maxYear: 1989, genres: ['Punk', 'Punk Rock', 'Horror Punk'] },
    // Late 70s and 80s Post-Punk/Goth Mix
    { minYear: 1975, maxYear: 1989, genres: ['Post-Punk', 'Goth Rock'] },
    // 70s Funk Mix
    { minYear: 1969, maxYear: 1979, genres: ['Funk'] },
    // 70s Soul Mix
    { minYear: 1969, maxYear: 1979, genres: ['R&B/Soul'] },
    // 70s Soft Rock Mix
    { minYear: 1965, maxYear: 1979, genres: ['Classic Rock', 'Soft Rock', 'Easy Listening', 'Psychedelic Rock'] },
    // 60s Psychedelic Rock Mix
    { minYear: 1959, maxYear: 1964, genres: ['Classic Rock', 'Soft Rock', 'Psychedelic Rock'] },
    // Misc. Workout (High Energy) Mix
    { minYear: 1960, maxYear: presentYear, genres: ['Industrial Metal', 'Punk', 'Punk Rock', 'Heavy Metal', 'Hip-Hop', 'Urbano', 'Thrash Metal', 'Nu Metal', 'Rock en español', 'Funk Metal', 'Hip-Hop français'] },
  ]
}
