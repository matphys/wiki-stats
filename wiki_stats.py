import sys
import math
import collections
import array

import statistics
from matplotlib import rc
rc('font', family='Droid Sans', weight='normal', size=14)

import numpy
import matplotlib.pyplot as plt



class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename, encoding="utf-8") as f:
            (n, _nlinks) = (0, 0) # TODO: прочитать из файла

            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))

            n, _nlinks = f.readline().split()
            n, _nlinks = int(n), int(_nlinks)

            self._n = n

            for i in range(n):
                self._titles.append(f.readline())
                size, flag, n0 = (i for i in map(int, f.readline().split()))
                self._sizes.append(size)
                self._redirect.append(flag)
                for j in range(n0):
                    self._links.append(int(f.readline()))
                self._offset.append(n0 + self._offset[-1])



        print('Граф загружен')


    def get_number_of_links_from(self, _id):
        return len(self._links[self._offset[_id]:self._offset[_id+1]])

    def get_links_from(self, _id):
        return self._links[self._offset[_id]:self._offset[_id+1]]

    def get_id(self, title):
        for i in range(len(self._titles)):
            if self._titles[i] == title:
                return(i)

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        return self._redirect[_id]

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes(_id)


    def get_count_redirection(self):
        return sum(self._redirect)



    def get_minimum_links_count(self):
        m = self._offset[1] - self._offset[0]
        for i in range(self._n):
            k = self._offset[i+1] - self._offset[i]
            m = min(k,m)
        return m


    def get_count_articles_with_min_links(self):
        s = 0
        t = self.get_minimum_links_count()
        for i in range(self._n):
            k = self._offset[i+1] - self._offset[i]
            if k == t:
                s += 1
        return s



    def get_maximum_links_count(self):
        m = self._offset[1] - self._offset[0]
        for i in range(self._n):
            k = self._offset[i + 1] - self._offset[i]
            m = max(k, m)
        return m




    def get_count_articles_with_max_links(self):
        s = 0
        t = self.get_maximum_links_count()
        for i in range(self._n):
            k = self._offset[i+1] - self._offset[i]
            if k == t:
                s += 1
        return s



    def article_with_max_links(self):
        m = self.get_maximum_links_count()
        for i in range(self._n):
            k = self._offset[i + 1] - self._offset[i]
            if k == m:
                return self._titles[i]



    def middle_count_links_in_article(self):
        middle_counr_links_in_article = [wg.get_number_of_links_from(i) for i in range(wg.get_number_of_pages()) if not wg.is_redirect(i)]
        return '%0.2f'%statistics.mean(middle_counr_links_in_article),'%0.2f'%statistics.stdev(middle_counr_links_in_article)

    def countlinks_to(self, i):
        countlinks_to = [0 for i in range(self.get_number_of_pages())]


    def min_count_links_to_article(self):
        countlinks_to = [0 for i in range(self.get_number_of_pages())]
        for i in range(self.get_number_of_pages()):
            for x in self.get_links_from(i):
                countlinks_to[x] += 1
                if self.is_redirect(i) == 1:
                    countlinks_to[x] -=1
        _mini = min(countlinks_to)
        return _mini
    def count_articles_with_min_links_count(self):
        countlinks_to = [0 for i in range(self.get_number_of_pages())]
        for i in range(self.get_number_of_pages()):
            for x in self.get_links_from(i):
                countlinks_to[x] += 1
                if self.is_redirect(i) == 1:
                    countlinks_to[x] -=1
        _mini = min(countlinks_to)
        num_of_links_with_min = sum(x == _mini for x in countlinks_to)
        return num_of_links_with_min

    def max_count_links_to_article(self):
        countlinks_to = [0 for i in range(self.get_number_of_pages())]
        for i in range(self.get_number_of_pages()):
            for x in self.get_links_from(i):
                countlinks_to[x] += 1
                if self.is_redirect(i) == 1:
                    countlinks_to[x] -=1
        _maxi = max(countlinks_to)
        return _maxi

    def count_articles_with_max_links_count(self):
        countlinks_to = [0 for i in range(self.get_number_of_pages())]
        for i in range(self.get_number_of_pages()):
            for x in self.get_links_from(i):
                countlinks_to[x] += 1
                if self.is_redirect(i) == 1:
                    countlinks_to[x] -=1
        _maxi = max(countlinks_to)
        num_of_links_with_max = sum(x == _maxi for x in countlinks_to)
        return num_of_links_with_max


    def article_with_max_links_count(self):
        index = 0
        counter = collections.defaultdict(int)
        for i in range(self._n):
            l = self._links[self._offset[i]:self._offset[i + 1]]
            if not self._redirect[i]:
                for i in l:
                    counter[i] += 1
        maxi = counter[0]
        for i in counter.keys():
            if counter[i] > maxi:
                maxi = counter[i]
                index = i
        return self.get_title(index)

    def middle_count_link_to_article(self):
        count_links_to = [0 for i in range(self.get_number_of_pages())]
        for i in range(self.get_number_of_pages()):
            if not self.is_redirect(i):
                for x in self.get_links_from(i):
                    count_links_to[x] += 1
        return '%0.2f'%statistics.mean(count_links_to), '%0.2f'%statistics.stdev(count_links_to)

    def min_count_redirect_to_article(self):
        counter = collections.defaultdict(int)
        for i in range(self._n):
            l = self._links[self._offset[i]:self._offset[i + 1]]
            if self._redirect[i]:
                for i in l:
                    counter[i] += 1
        mini = counter[0]
        for i in counter.keys():
            if counter[i] < mini:
                mini = counter[i]
        return mini




    def count_articles_with_min_redirects_count(self):
        redirects_to = [0 for i in range(self.get_number_of_pages())]
        for i in range(self.get_number_of_pages()):
            for x in self.get_links_from(i):
                if self.is_redirect(i) == 1:
                    redirects_to[x] += 1
        _mini = min(redirects_to)
        pages_with_min_redir = sum(x == _mini for x in redirects_to)
        return pages_with_min_redir


    def max_count_redirects_to_article(self):
        counter = collections.defaultdict(int)
        for i in range(self._n):
            l = self._links[self._offset[i]:self._offset[i + 1]]
            if self._redirect[i]:
                for i in l:
                    counter[i] += 1
        maxi = counter[0]
        for i in counter.keys():
            if counter[i] > maxi:
                maxi = counter[i]
        return maxi




    def count_articles_with_max_redirects_count(self):
        k = 0
        counter = collections.defaultdict(int)
        for i in range(self._n):
            l = self._links[self._offset[i]:self._offset[i + 1]]
            if self._redirect[i]:
                for i in l:
                    counter[i] += 1
        maxi = counter[0]
        for i in counter.keys():
            if counter[i] > maxi:
                mini = counter[i]
        for i in counter.keys():
            if maxi == counter[i]:
                k += 1
        return k



    def article_with_max_redirects_count(self):
        index = 0
        counter = collections.defaultdict(int)
        for i in range(self._n):
            l = self._links[self._offset[i]:self._offset[i + 1]]
            if self._redirect[i]:
                for i in l:
                    counter[i] += 1
        maxi = counter[0]
        for i in counter.keys():
            if counter[i] > maxi:
                maxi = counter[i]
                index = i
        return self.get_title(index)

    def bfs(self,a,b):
        fired = {a}
        queue = [a]
        path = []
        while queue:
            current = queue.pop(0)
            print(self.get_links_from(self.get_id(current)))
            for neighbour in self.get_links_from(self.get_id(current)):
                if neighbour not in fired:
                    fired.add(neighbour)
                    queue.append(neighbour)
                    path.append(neighbour)
                    if neighbour == b:
                        break
        return path





    def middle_count_redirects_to_article(self):
        redirects_to = [0 for i in range(self.get_number_of_pages())]
        for i in range(self.get_number_of_pages()):
            for x in self.get_links_from(i):
                if self.is_redirect(i) == 1:
                    redirects_to[x] += 1
        return '%0.2f'%statistics.mean(redirects_to), '%0.2f'%statistics.stdev(redirects_to)



def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True, **kwargs):
    plt.clf()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.hist(x=data,bins=bins,color=facecolor,label=title,**kwargs)
    plt.savefig(fname)
    plt.show()



if __name__ == '__main__':
    wg = WikiGraph()
    wg.load_from_file('wiki_small.txt')
    print('Количество статей с перенаправлением:', wg.get_count_redirection())
    print('Минимальное количество ссылок из статьи:', wg.get_minimum_links_count())
    print('Количество статей с минимальным количеством ссылок:', wg.get_count_articles_with_min_links())
    print('Максимальное количество ссылок из статьи:', wg.get_maximum_links_count())
    print('Количество статей с максимальным количеством ссылок:', wg.get_count_articles_with_max_links())
    print('Статья с наибольшим количеством ссылок:', wg.article_with_max_links())
    print('Среднее количество ссылок в статье, среднеквадратичное отклонение :', wg.middle_count_links_in_article())
    print('Минимальное количество ссылок на статью:', wg.min_count_links_to_article())
    print('Количество статей с минимальным количеством внешних ссылок:', wg.count_articles_with_min_links_count())
    print('Максимальное количество ссылок на статью:', wg.max_count_links_to_article())
    print('Количество статей с максимальным количеством внешних ссылок:', wg.count_articles_with_max_links_count())
    print('Статья с наибольшим количеством внешних ссылок:', wg.article_with_max_links_count())
    print('Среднее количество внешних ссылок на статью, среднеквадратичное отклонение:', wg.middle_count_link_to_article())
    print('Минимальное количество перенаправлений на статью:', wg.min_count_redirect_to_article())
    print('Количество статей с минимальным количеством внешних перенаправлений:', wg.count_articles_with_min_redirects_count())
    print('Максимальное количество перенаправлений на статью:', wg.max_count_redirects_to_article())
    print('Количество статей с максимальным количеством внешних перенаправлений: ', wg.count_articles_with_max_redirects_count())
    print('Статья с наибольшим количеством внешних перенаправлений:', wg.article_with_max_redirects_count())
    print('Среднее количество внешних перенаправлений на статью,среднеквадратичное отклонение :', wg.middle_count_redirects_to_article())
    hist('Распределение количества ссылок из статьи.png', [wg.get_number_of_links_from(i) for i in range(wg._n)], 100, 'Количество статей', "Количество ссылок", "Распределение количества ссылок из статьи", range=(0,200))
    hist('Распределение количества ссылок на статью.png', [[0 for i in range(wg.get_number_of_pages())][i] for i in range(wg._n)], 100, 'Количество статей', "Количество ссылок", "Распределение количества ссылок на статью", range=(0,200))
    hist('Распределение количества перенаправлений на статью.png', [[0 for i in range(wg.get_number_of_pages())][i] for i in range(wg._n)], 20, 'Количество статей', "Количество ссылок", "Распределение количества редиректов на статью", range=(0,20))
    hist('Распределение размеров статей.png', [wg._sizes[i] for i in range(wg._n)], 100, 'Количество статей', "Количество ссылок", "Распределение размеров статей", range=(0,100000))
    hist('Распределение размеров статей(в логарифмическом масштабе.png', numpy.log10([wg._sizes[i] for i in range(wg._n)]), 25, 'Количество статей', "Количество ссылок", "Распределение размеров статей (log)", range=(0,6))
