require 'rake'
require 'time'
require 'pathname'
require 'yaml'
require 'jekyll'

# http://rake.rubyforge.org/files/doc/rakefile_rdoc.html
# http://www.layouts-the.me/rake/2011/04/23/rake_tasks_for_jekyll/
# https://github.com/plusjade/jekyll-bootstrap/blob/master/Rakefile
SOURCE = "."
CONFIG = {
  'themes'     => File.join(SOURCE, "_includes", "themes"),
  'layouts'    => File.join(SOURCE, "_layouts"),
  'posts'      => File.join(SOURCE, "_posts"),
  'post_ext'   => "md",
  'font'       => './fonts/glyphs.ttf',
  'font_theme' => 'glyphs',
  'test_post'  => '_posts/2012-01-01-test.markdown',
}

ENV['PATH'] = [ENV['PATH'], './bin'].join(':')

def export_glyphs(font, prefix=CONFIG['glyphs'])
  glyphs = `./glyphs.py -p #{prefix} #{font}`.collect do |line|
    line.split
  end
end

def get_glyphs(font)
  glyphs = `./glyphs.py -n #{font}`.collect do |line|
    line.split
  end
end

def titlize(string)
  string.gsub("_", ' ').gsub(/\b('?[a-z])/) { $1.capitalize }
end

def font_metadata(font)
  path  = Pathname.new(font)
  basename = Pathname.new(font).basename
  prefix = path.dirname
  
  title = basename.to_s.gsub(basename.extname, '')
  glyphs = get_glyphs(font).collect do |original, name, x, code|
    [ "icon-#{name}", code ]
  end
  { 'font' => { 'title' => titlize(title),
                'name'  => title, 'prefix' => prefix.to_s,
                'path'  => font,  'glyphs' => glyphs, } }
end

desc "Fake task"
task :foobar, [:one, :two] do |t, args|
  puts "args: #{args}"
end

desc "Launch preview environment"
task :preview do
  system "jekyll --auto --server"
end # task :preview

# https://github.com/plusjade/jekyll-bootstrap/blob/master/Rakefile#L38
# with some tweaks.
# Usage: rake post title="A Title" [date="2012-02-09"]
desc "Begin a new post in #{CONFIG['posts']}"
task :post, [:title, :date, :overwrite] do |t, args|
  abort("rake aborted: '#{CONFIG['posts']}' directory not found.") unless FileTest.directory?(CONFIG['posts'])
  args.with_defaults(:title => ENV["title"] || "new-post",
                     :date  => ENV["date"]  || "today",
                     :overwrite => ENV["overwrite"])
  title = args.title
  date  = args.date
  slug  = title.downcase.strip.gsub(' ', '-').gsub(/[^\w-]/, '')
  begin
    date = Time.parse(date).strftime('%Y-%m-%d')
  rescue Exception => e
    puts %Q(Error - I couldn't understand this date: #{date}.
    Try YYYY-MM-DD or "today".)
    exit -1
  end
  filename = File.join(CONFIG['posts'], "#{date}-#{slug}.#{CONFIG['post_ext']}")
  choice = 'y'
  if File.exist?(filename) 
    if args.overwrite
      choice = args.overwrite
    else
      choices = ['y', 'n']
      msg = %Q(#{filename} already exists. Do you want to overwrite?)
      #abort("rake aborted!") if () == 'n'
      choice = ask(msg, choices)
    end
  end
  
  if choice == 'y'
    front = { 'layout' => 'font',
              'title' => title.gsub(/-/,' '),
              'description' => "",
              'category' => '',
              'tags' => [] }
    opts = { :front => front,
             :content => %Q( )
           }
    write_post(filename, opts)
  end
end # task :post

def write_post(filename, opts)
  puts "Creating new post: #{filename}"
  front = opts[:front]
  content = opts[:content]
  post = Post.new(filename)
  post.content = content
  post.update_data(front)
  post.write( )
  true
end

def update_post_yaml(filename, data)
  puts "Updating yaml for post: #{filename}"
  post = Post.new(filename)
  post.update_data(data)
  post.write( )
  true
end

class Post
  # https://github.com/mojombo/jekyll/blob/master/lib/jekyll/convertible.rb#L1
  include Jekyll::Convertible
  attr_accessor :data, :content, :ext, :output
  def initialize(filename)
    @filename = filename
    self.content = ''
    self.data  = { }
    @path = Pathname.new(filename)
    if @path.file?
      self.read( )
    end
  end
  def read
    self.read_yaml(@path.dirname.to_s, @path.basename.to_s)
    self.output = self.content
    self.data
  end
  def update_data(data)
    self.data = self.data.update(data)
  end
  def write
    puts @path.to_s
    @path.open('w') do |post|
      post.puts YAML.dump(self.data)
      post.puts "---"
      post.puts self.content
    end
    true
  end
end

namespace :font do
  desc "Export a font's glyphs to a directory."
  task :export, [:font, :prefix] do |t, args|
    args.with_defaults(:font   => ENV['font']   || CONFIG['font'],
                       :prefix => ENV['prefix'] || "./#{CONFIG['font_theme']}")
    Pathname.new(args.prefix).mkpath
    export_glyphs(args.font, args.prefix).each do |original, name, x, code|
      puts [original, name, code].join(" ")
    end
  end

  desc "Build a font given a directory of glyphs."
  task :build, [:theme] do |t, args|
    args.with_defaults(:theme=> ENV['theme'] || CONFIG['font_theme'])
    output = `./glyphs2webfont.sh #{args.theme}`
    lines = output.collect
    puts "Built font using #{lines.length - 1} glyphs"
    puts "#{lines[0]}"
  end

  desc "print list glyphs from a font."
  task :glyphs, [:font] do |t, args|
    args.with_defaults(:font => ENV['font'] || CONFIG['font'])
    get_glyphs(args.font).each do |original, name, x, code|
      puts [name, code].join(" ")
    end
  end

  desc "print glyphs in css given path to font"
  task :css, [:font] do |t, args|
    args.with_defaults(:font => ENV['font'] || CONFIG['font'])
    command = %Q(./glyphs.py -q -n #{args.font} \
                         | sed -e "s|^|icon-|g" \
                         | ./glyph2css.sh)
    system(command)
  end

  desc "print glyphs in yaml given path to font"
  task :yaml, [:font] do |t, args|
    args.with_defaults(:font => ENV['font'] || CONFIG['font'])
    puts YAML.dump(font_metadata(args.font))
  end

  desc "add/update yaml in a post"
  task :demo, [:font, :post] do |t, args|
    args.with_defaults(:font => ENV['font'] || CONFIG['font'],
                       :post => ENV['post'] || CONFIG['test_post'])
    update_post_yaml(args.post, font_metadata(args.font))
  end

  desc %Q(publish directory of glyphs as new font with demo post)
  task :publish, [:theme] do |t, args|
    args.with_defaults(:theme=> ENV['theme'] || CONFIG['font_theme'])
    fontname = "fonts/#{args.theme}.ttf"
    Rake::Task["font:build"].invoke(args.theme)
    Rake::Task["post"].invoke(args.theme, 'today', 'f')
    search = "#{CONFIG['posts']}/*#{args.theme}.#{CONFIG['post_ext']}"
    post = FileList[search].sort.pop
    Rake::Task["font:demo"].invoke(fontname, post)
    puts "#{post} has a demo of #{fontname}"
  end

  desc %Q(given a font, export and publish the glyphs in a post)
  task :analyze, [:font, :theme] do |t, args|
    args.with_defaults(:font   => ENV['font'] || CONFIG['font'],
                       :theme  => ENV['theme'])
    path  = Pathname.new(args.font)
    base  = path.basename.to_s.gsub(path.extname, '')
    theme = args.theme || base
    Rake::Task["font:export"].invoke(args.font, theme)
    Rake::Task["font:publish"].invoke(theme)
  end
end


def ask(message, valid_options)
  if valid_options
    answer = nil
    responses = valid_options.collect(&:to_s).join('/').
                              gsub(/"/, '').gsub(/, /,'/')
    while !valid_options.include?(answer)
      answer = get_stdin("#{message} #{responses} ")
    end
  else
    answer = get_stdin(message)
  end
  answer
end

def get_stdin(message)
  print message
  STDIN.gets.chomp
end

#####
# EOF
