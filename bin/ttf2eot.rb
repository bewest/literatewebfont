#!/usr/bin/ruby

require 'optparse'
require 'rubygems'
gem 'ttf2eot'
require 'ttf2eot'

def input_name(input)
  return input
end

def output_name(input)
  return input.gsub(/\.ttf$/, '.woff')
end

def ttf2eot(input)
  TTF2EOT.convert(input_name(input), output_name(input))
end

ARGV.each do |file|
  ttf2eot file
end

#####
# EOF
